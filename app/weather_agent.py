import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field

load_dotenv()

SYSTEM_PROMPT = "You are a helpful weather assistant."
MODEL_NAME = "gpt-4o"
APP_INFO_PATH = Path(__file__).resolve().parent / "data" / "app_info.json"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]


class CurrentWeather(BaseModel):
    model_config = ConfigDict(extra="forbid")

    time: int | str | None = None
    temperature_2m: float | None = None
    temperature_2m_f: float | None = None
    apparent_temperature: float | None = None
    apparent_temperature_f: float | None = None
    relative_humidity_2m: float | None = None
    wind_speed_10m: float | None = None
    weather_code: int | None = None
    uv_index: float | None = None


class CurrentUnits(BaseModel):
    model_config = ConfigDict(extra="forbid")

    time: str | None = None
    temperature_2m: str | None = None
    temperature_2m_f: str | None = None
    apparent_temperature: str | None = None
    apparent_temperature_f: str | None = None
    relative_humidity_2m: str | None = None
    wind_speed_10m: str | None = None
    weather_code: str | None = None
    uv_index: str | None = None


class WeatherPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None
    location_label: str | None = None
    map_image_url: str | None = None
    current: CurrentWeather | None = None
    current_units: CurrentUnits | None = None


class AppInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    app_name: str | None = None
    summary: str | None = None
    how_it_works: list[str] = []
    capabilities: list[str] = []
    data_sources: list[str] = []
    limitations: list[str] = []
    tech_stack: list[str] = []


class WeatherResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    temperature: float | None = Field(
        default=None,
        description="The current temperature in celsius for the given location if available.",
    )
    response: str = Field(
        description="A natural language response to the user's question."
    )
    weather: WeatherPayload | None = Field(
        default=None,
        description="Structured weather payload for UI weather cards.",
    )
    app_info: AppInfo | None = Field(
        default=None,
        description="Structured application information for about/help cards.",
    )


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def _load_app_info() -> dict | None:
    try:
        with APP_INFO_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _is_about_query(user_message: str) -> bool:
    text = user_message.lower()
    keywords = [
        "what are you",
        "how does this work",
        "what can you do",
        "about",
        "who made you",
        "what is this app",
        "features",
        "capabilities",
    ]
    return any(keyword in text for keyword in keywords)


def _title_case(value: str | None) -> str | None:
    if not value:
        return None
    return " ".join(part.capitalize() for part in value.strip().split())


def _reverse_geocode_location_label(latitude: float, longitude: float) -> str | None:
    """Resolve human-readable location label like 'Paris, France' from coordinates."""
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "format": "jsonv2",
                "lat": latitude,
                "lon": longitude,
                "zoom": 10,
                "addressdetails": 1,
            },
            headers={"User-Agent": "weather-agent/1.0"},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        address = payload.get("address", {})
    except Exception:
        return None

    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("municipality")
        or address.get("county")
    )
    country = address.get("country")

    city = _title_case(city)
    country = _title_case(country)

    if city and country:
        return f"{city}, {country}"
    if city:
        return city
    if country:
        return country
    return None


def _build_google_static_map_url(latitude: float, longitude: float) -> str | None:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return None

    return (
        "https://maps.googleapis.com/maps/api/staticmap"
        "?size=1200x500"
        "&scale=2"
        "&maptype=roadmap"
        f"&center={latitude},{longitude}"
        "&zoom=11"
        f"&markers=color:red|{latitude},{longitude}"
        "&style=feature:poi|visibility:off"
        "&style=feature:transit|visibility:simplified"
        "&style=feature:road|element:geometry|color:0x2a2a2a"
        "&style=feature:water|color:0x1a1a1a"
        f"&key={api_key}"
    )


def get_weather(latitude: float, longitude: float) -> dict:
    """Get current weather conditions from Open-Meteo for specific coordinates."""
    response = requests.get(
        (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            "&timeformat=unixtime"
            "&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code,uv_index"
        ),
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    current = data.get("current", {})
    current_units = data.get("current_units", {})

    temp_c = current.get("temperature_2m")
    apparent_c = current.get("apparent_temperature")

    temp_f = (float(temp_c) * 9 / 5 + 32) if temp_c is not None else None
    apparent_f = (float(apparent_c) * 9 / 5 + 32) if apparent_c is not None else None

    current_with_converted = {
        **current,
        "temperature_2m_f": temp_f,
        "apparent_temperature_f": apparent_f,
    }
    current_units_with_converted = {
        **current_units,
        "temperature_2m_f": "°F",
        "apparent_temperature_f": "°F",
    }
    location_label = _reverse_geocode_location_label(latitude, longitude)
    map_image_url = _build_google_static_map_url(latitude, longitude)

    return {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "timezone": data.get("timezone"),
        "location_label": location_label,
        "map_image_url": map_image_url,
        "current": current_with_converted,
        "current_units": current_units_with_converted,
    }


def _call_function(name: str, args: dict) -> dict:
    if name == "get_weather":
        return get_weather(**args)
    raise ValueError(f"Unsupported function call: {name}")


def run_weather_chat(user_message: str) -> WeatherResponse:
    client = _get_client()
    weather_payload: dict | None = None

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    app_info = _load_app_info()
    use_weather_tools = True
    if _is_about_query(user_message) and app_info:
        use_weather_tools = False
        messages.append(
            {
                "role": "system",
                "content": (
                    "The user is asking about this application. "
                    "Use only the following JSON knowledge base for app-related facts:\n"
                    f"{json.dumps(app_info)}"
                ),
            }
        )
        messages.append(
            {
                "role": "system",
                "content": (
                    "Answer app questions in a readable structured format using short section headers and bullets. "
                    "Use plain text only. Keep it concise, but organized."
                ),
            }
        )

    messages.append({"role": "user", "content": user_message})

    if not use_weather_tools:
        completion = client.beta.chat.completions.parse(
            model=MODEL_NAME,
            messages=messages,
            response_format=WeatherResponse,
        )
        parsed = completion.choices[0].message.parsed
        if parsed is None:
            raise RuntimeError("Model returned an empty parsed weather response.")
        parsed.app_info = AppInfo.model_validate(app_info)
        return parsed

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=TOOLS,
    )

    assistant_message = completion.choices[0].message
    tool_calls = assistant_message.tool_calls or []

    if tool_calls:
        messages.append(assistant_message)

    for tool_call in tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        result = _call_function(name, args)
        if name == "get_weather":
            weather_payload = result
        messages.append(
            {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
        )

    completion_2 = client.beta.chat.completions.parse(
        model=MODEL_NAME,
        messages=messages,
        tools=TOOLS,
        response_format=WeatherResponse,
    )

    parsed = completion_2.choices[0].message.parsed
    if parsed is None:
        raise RuntimeError("Model returned an empty parsed weather response.")

    if weather_payload:
        current = weather_payload.get("current", {})
        parsed.temperature = current.get("temperature_2m", parsed.temperature)
        parsed.weather = weather_payload

    return parsed
