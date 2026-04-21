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