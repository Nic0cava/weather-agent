# 1: Initiated Git Repository
- created weather-agent project folder
- cd to folder
- created new weather-agent repo on GitHub
- ran git commands to initiate and connect repo to project folder

---

# 2: Virtual Environment Set-Up
## Default
```bash
uv venv
```

Creates:
```
.venv/
```

---


# 3. Activate Environment (Git Bash)

```bash
source .venv/Scripts/activate
```

You should see the name of the folder you created the venv in:
```
(weather-agent)
```

---

# 4. Install Dependencies

## Create `pyproject.toml`
```bash
uv init
```
---

## If installing manually
```bash
uv pip install ipykernel jupyter numpy matplotlib
```
## or add to `pyproject.toml` manually (recommended)
```bash
uv add ipykernel jupyter numpy matplotlib
```

## If using `pyproject.toml` (recommended)
```bash
uv sync
```
---

# 5. Register Jupyter Kernel 

```bash
python -m ipykernel install --user --name=.venv --display-name "Python (.venv)"
```
- Note: This can take a few seconds to show up as kernel options so be patient
- In this case you should see (weather-agent) even after running the command above

---


# 6. Test Your Environment

Create file:

```
test_env.py
```

Paste:

```python
import numpy as np
import matplotlib as mpl

print("SUCCESS: Virtual environment is working correctly!")
print(f"NumPy: {np.__version__}, Matplotlib: {mpl.__version__}")
```

Run:

```bash
uv run test_env.py
```

---

## ✅ Expected Output

```
SUCCESS: Virtual environment is working correctly!
NumPy: X.X.X, Matplotlib: X.X.X
```

---

# 7. Test Jupyter Notebook

- Using the same test_env.py file
- Select/highlight code snippet you want to test
- press 'Select' + 'Enter' keys to run code snippet in Jupyter
- It will likely fail, this is expected
- Now switch the kernel to your venv, in this case (weather-agent)
- now test the code snippets again
- they should now work and match what you tested in the terminal output

# 🔁 Daily Workflow

Each time you return to the project:

```bash
source .venv/Scripts/activate
```
- Note: you probably won't need to do this every time since we are using uv, as long as you see that the venv is activated
- in this case you should see (weather-agent)
---

# ⚠️ Troubleshooting

## Kernel not showing
```bash
uv pip install ipykernel
python -m ipykernel install --user --name=.venv --display-name "Python (.venv)"
jupyter kernelspec list
```

---

## Wrong Python being used
```bash
which python
```

Expected (in this case):
```
weather-agent/.venv/Scripts/python
```


---

# ✅ Summary Workflow

```bash
uv venv
source .venv/Scripts/activate
uv sync
python -m ipykernel install --user --name=.venv --display-name "Python (.venv)" # <- only if your not already connected
```

Then:
- Select interpreter in VS Code
- Open notebook
- Select kernel
- Done ✅

# 8. Add `.gitignore` file

## Paste this standard boiler plate .gitignore
```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover

# Translations
*.mo
*.pot

# Django stuff:
*.log

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# DotEnv configuration
.env

# Database
*.db
*.rdb

# Pycharm
.idea

# VS Code
.vscode/
*.code-workspace

# Spyder
.spyproject/

# Jupyter NB Checkpoints
.ipynb_checkpoints/

# Mac OS-specific storage files
.DS_Store

# vim
*.swp
*.swo

# Mypy cache
.mypy_cache/

# Exclude virtual environment
.venv/

# Exclude trained models
/models/

# exclude data from source control by default
# /data/

# exclude lancedb from source control by default
lancedb/
```

# 9. Create `app` folder and set up organized project structure within

## create `main.py` file within
- set-up FastAPI boiler plate connection
```python
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Boilerplate FastAPI App")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"page_title": "FastAPI Template Test"},
    )

```

## create `templates` folder within
- create `index.html` file within
- set-up html and Jinja2Templates boiler plate connection
```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ page_title }}</title>
</head>
<body>
  <main>
    <h1>FastAPI + Jinja2 Boilerplate</h1>
    <p>If you can see this, your template connection is working.</p>
  </main>
</body>
</html>

```

## Run and test your connection
```bash
uv run uvicorn main:app --reload
```
- you should see running on http://127.0.0.1:8000
- you should also be getting "200 OK"
- visit the link to see that it works

## Alternatively, you could add this at the bottom of the `main.py` file
```python
# Run our application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

```

-Then run the command
```bash
uv run main.py
```
- You should get the same result

# 10. Create `.env` file
- place all your SECRET_KEYS within this file
- IMPORTANT: make sure `.env` is listed in the `.gitignore` file or you will leak your keys to GitHub

# 11. Used Google's Stitch AI design tool to create a rough draft of the front end
- Used codex to stitch the copied html code for mobile and desktop views within the index.html file
- Then forced codex to review the code snippets to fix any gaps made
- Tested both mobile and desktop views after running app, completing the front-end rough draft

# 12.# 12. Weather Agent + Chat Integration Summary

## Backend
- Integrated weather agent into FastAPI by adding `POST /api/chat` in `app/main.py`.
- Added `ChatRequest` and `ChatResponse` models for message input and structured response output.
- `/api/chat` now returns:
  - `response` (assistant text)
  - `temperature`
  - `weather` (structured payload for UI cards)

## Weather Agent
- Refactored `app/weather_agent.py` from script-style execution to reusable functions.
- Added `run_weather_chat(user_message)` entrypoint for API use.
- Kept OpenAI tool-calling flow and connected it to Open-Meteo weather lookup.
- Expanded weather fields requested from Open-Meteo current conditions:
  - `temperature_2m`
  - `apparent_temperature`
  - `relative_humidity_2m`
  - `wind_speed_10m`
  - `weather_code`
  - `uv_index`
- Structured output hardening:
  - Replaced loose `dict` schema with strict nested Pydantic models (`CurrentWeather`, `CurrentUnits`, `WeatherPayload`) to satisfy OpenAI `response_format` schema requirements.

## Frontend (existing design preserved)
- Restored original `index.html` design and wired chat functionality into existing input/send controls.
- Added client-side fetch integration to `/api/chat` for both mobile and desktop chat boxes.
- Added dynamic assistant response rendering in existing style.
- Added dynamic weather card rendering that matches the existing card aesthetic and appears when weather data is returned.
- Card data now binds live API values (condition, temp, feels-like, humidity, wind, UV, timestamp).
- Updated card location label behavior to use user-entered location text instead of coordinates.
- Normalized two-part comma locations to standard order:
  - `Italy, Rome` -> `Rome, Italy`


# 13. Weather Card UX + Location Quality Updates

## Weather Data + Backend Enhancements
- Added precomputed Fahrenheit values in `app/weather_agent.py` so both units are available immediately in each response:
  - `temperature_2m_f`
  - `apparent_temperature_f`
- Extended structured weather payload schema to include converted temperature fields and units.
- Added reverse geocoding (Nominatim / OpenStreetMap) from returned coordinates to resolve user-friendly location labels.
- Added `location_label` to weather payload so cards can display city/country labels such as `Paris, France` when available.

## Frontend Chat UX Improvements
- Added auto-scroll behavior so chat keeps latest messages in view as bubbles/cards are appended.
- Added animated `Thinking...` indicator while the model is generating a response.
- Removed seeded Paris example content and replaced with a welcome/call-to-action starter message.
- Updated mobile and desktop input placeholders to:
  - `What is the current weather like in Paris?`

## Weather Card Rendering Updates
- Wired dynamic weather cards to consume structured payload fields from `/api/chat`.
- Added interactive per-card temperature unit toggle (`�C` <-> `�F`) without additional API calls.
- Toggle now switches:
  - Main display temperature
  - Feels-like temperature
  - Unit text labels
- Repositioned toggle under the main large temperature display per latest UI preference.
- Reduced spacing beneath toggle and tightened spacing before lower card divider/grid.
- Moved weather icon slightly higher toward the upper-right corner to match original visual feel.

## Location Display Formatting
- Card location display now prioritizes backend `location_label` (city + country) when available.
- Added frontend fallback title-casing for user-derived location strings when reverse geocoding is unavailable.

## Reliability / Cleanup
- Fixed encoding artifacts introduced during iterative edits (unit symbols and separators).
- Re-ran Python compile checks for backend files after changes.

# 14. About Retrieval + Response Formatting Improvements

## App Retrieval (JSON-backed Q&A)
- Added `app/data/app_info.json` as a structured knowledge base for application-level questions.
- Updated `app/weather_agent.py` to detect app/about intent (e.g., "What can you do?", "How does this work?").
- For app-intent questions:
  - Injects JSON knowledge into system context.
  - Uses structured parse response path.
  - Returns `app_info` in the response payload for frontend-aware formatting.

## About Button Behavior
- Kept About button behavior separate from chat Q&A.
- About button now shows a simple summary-style About card only (title + concise summary), with no extra nested blocks that looked like clickable buttons.
- Applied to both mobile and desktop About actions.

## Chat Output Styling + Readability
- Added assistant text formatter in `app/templates/index.html` for cleaner normal answers:
  - Converts markdown-style `**bold**` to real bold text.
  - Converts numbered steps (`1.`, `2.`, etc.) into ordered list rendering.
  - Improves paragraph spacing and readability in both mobile and desktop chat bubbles.
- Added organized app-answer rendering logic so app-related user questions show structured text from JSON-backed context instead of reusing the About button pop-up card.

## Error Handling Hardening
- Fixed backend response serialization for `app_info` in `app/main.py` by converting Pydantic model to dict (`model_dump`) before returning API response.
- Hardened frontend `/api/chat` fetch handling:
  - If server returns JSON, parse JSON.
  - If server returns non-JSON text (e.g., Internal Server Error), parse text and surface readable error.
  - Prevents client-side `Unexpected token ... is not valid JSON` failures.

## Verification
- Re-ran compile/sanity checks after updates:
  - `./.venv/Scripts/python.exe -m compileall app/weather_agent.py app/main.py`
