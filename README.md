# Weather Agent

[Visit Live Site](https://weather-agent-8535.onrender.com)

> Note: This app runs on Render free tier, so cold starts can take about 30-60 seconds.

---

## Overview

Weather Agent is a chat-first AI weather assistant that turns a simple question into:
- a natural language answer
- a polished weather response card

It is built to feel lightweight for users while still using structured backend logic for reliable outputs.

---

## What The Agent Does

| User Intent | Agent Behavior |
|---|---|
| Weather question | Fetches live weather data and returns a readable answer + weather card |
| App/about question | Uses local JSON retrieval (`app/data/app_info.json`) to answer project questions clearly |

The agent routes requests based on message intent, then returns structured data for frontend rendering.

---

## Weather Flow (Simple)

1. User asks for weather in a location.
2. The model decides weather data is needed.
3. Tool-calling fetches current data from Open-Meteo.
4. Reverse geocoding enriches the location label (city/country when available).
5. Celsius and Fahrenheit are both prepared so the UI can toggle instantly.
6. A map URL is generated (if Google Maps key is configured).
7. Frontend renders a detailed card (temp, feels-like, humidity, wind, UV, map).

---

## About / Retrieval Flow

1. User asks "What can you do?", "How does this work?", etc.
2. Agent retrieves facts from `app/data/app_info.json`.
3. Response is returned in organized, readable chat format.
4. The About button remains separate and shows a simple summary card by design.

---

## UI Experience

- Responsive mobile + desktop chat layouts
- Auto-scroll to latest message
- "Thinking..." loading feedback
- Cleaner formatted assistant text (bold emphasis, numbered steps)
- Weather cards with C/F toggle
- Optional map image in weather cards

---

## Services And Tools

- OpenAI API: chat reasoning + tool-calling
- Open-Meteo API: current weather data
- OpenStreetMap Nominatim: reverse geocoding labels
- Google Static Maps API: location map image (optional)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Templating | Jinja2 |
| Validation | Pydantic |
| Frontend | HTML, Tailwind CSS, Vanilla JavaScript |
| Config | python-dotenv |
| Runtime / deps | uv |

---

## Why I Built This Project

I built this project to practice creating real-world AI agents using an augmented LLM workflow, inspired by Anthropic's paper on agent design: [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents).

I wanted to explore how to make an LLM more useful by adding tool use and retrieval, then turn those outputs into a clean user experience instead of plain text answers.

This project taught me a lot about orchestration, response formatting, and practical tradeoffs in agent design. I plan to carry these lessons into future projects and build systems that are more capable, reliable, and user-friendly.
