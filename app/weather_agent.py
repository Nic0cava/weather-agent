import json
import os

import requests
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ConfigDict
from pydantic import BaseModel, Field

load_dotenv()

SYSTEM_PROMPT = "You are a helpful weather assistant."
MODEL_NAME = "gpt-4o"

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

    time: str | None = None
    temperature_2m: float | None = None
    apparent_temperature: float | None = None
    relative_humidity_2m: float | None = None
    wind_speed_10m: float | None = None
    weather_code: int | None = None
    uv_index: float | None = None


class CurrentUnits(BaseModel):
    model_config = ConfigDict(extra="forbid")

    time: str | None = None
    temperature_2m: str | None = None
    apparent_temperature: str | None = None
    relative_humidity_2m: str | None = None
    wind_speed_10m: str | None = None
    weather_code: str | None = None
    uv_index: str | None = None


class WeatherPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None
    current: CurrentWeather | None = None
    current_units: CurrentUnits | None = None


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


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def get_weather(latitude: float, longitude: float) -> dict:
    """Get current weather conditions from Open-Meteo for specific coordinates."""
    response = requests.get(
        (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            "&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code,uv_index"
        ),
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "timezone": data.get("timezone"),
        "current": data.get("current", {}),
        "current_units": data.get("current_units", {}),
    }


def _call_function(name: str, args: dict) -> dict:
    if name == "get_weather":
        return get_weather(**args)
    raise ValueError(f"Unsupported function call: {name}")


def run_weather_chat(user_message: str) -> WeatherResponse:
    client = _get_client()
    weather_payload: dict | None = None

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

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
