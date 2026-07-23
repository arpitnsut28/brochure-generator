# Company Brochure Generator

An automated tool that turns any company website into a short, polished
marketing brochure. Give it a company name and a URL — it scrapes the site,
uses Google's Gemini model to figure out which pages actually matter (About,
Careers, Company, etc.), scrapes those too, and then generates a clean
markdown brochure summarizing the company for prospective customers,
investors, and recruits.

Available in two forms:
- **Jupyter Notebook** — an interactive lab for prototyping and testing each
  step of the pipeline.
- **Flask web app** — a simple browser UI where you type in a company name
  and URL and get a formatted brochure back.

---

## How it works

```
Website URL
    ↓
Scrape links + landing page text
    ↓
Gemini call #1 → pick relevant pages (returns JSON)
    ↓
Scrape those pages too
    ↓
Gemini call #2 → write the brochure (returns markdown)
    ↓
Display in notebook / render on webpage
```

1. **Scrape the site** — `fetch_website_links()` and `fetch_website_contents()`
   (in `scraper.py`) pull the raw links and text off the target site using
   `requests` + `BeautifulSoup`.
2. **First Gemini call** — the model is shown every link found on the
   homepage and decides which ones are relevant for a brochure (About,
   Careers, Company, etc.), returning structured JSON. Terms of Service,
   Privacy, and email links are filtered out.
3. **Gather content** — each relevant page gets scraped too, and everything
   is combined into one markdown-structured block of text.
4. **Second Gemini call** — the model reads all the gathered content and
   writes a short brochure in markdown, covering company culture, customers,
   and careers where available.
5. **Display** — shown as rendered markdown in the notebook, or sent back to
   the browser and rendered on the webpage.

---

## Tech stack

- **Python 3** — core logic
- **[Gemini API](https://ai.google.dev/)** (`google-genai`) — the two LLM calls
- **BeautifulSoup + Requests** — web scraping
- **python-dotenv** — loads the API key from `.env`
- **Jupyter Notebook** — interactive prototyping environment
- **Flask** — backend web server for the browser version
- **HTML / CSS / JavaScript** — front-end for the web app (vanilla, no framework)

---

## Project structure

```
brochure/
├── app.py                 # Flask server (routes: / and /generate)
├── brochure_logic.py      # Core pipeline: scraping + both Gemini calls
├── scraper.py              # fetch_website_links / fetch_website_contents
├── brochure.ipynb          # Notebook version, for interactive testing
├── .env                    # Your API key (never committed — see below)
├── .env.example             # Template showing what .env should contain
├── .gitignore
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    └── index.html
```

---

## Setup

### 1. Clone the repo and enter the folder

```bash
git clone <your-repo-url>
cd brochure
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

> On Windows, if PowerShell blocks the activation script, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 3. Install dependencies

```bash
pip install python-dotenv google-genai beautifulsoup4 requests flask ipykernel
```

### 4. Add your API key

Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey),
then create a `.env` file in the project root:

```
GEMINI_API_KEY=your_actual_key_here
```

`.env` is listed in `.gitignore` and should never be committed.

---

## Usage

### Option A — Run the notebook

Open `brochure.ipynb` in VS Code or Jupyter, select the `.venv` kernel, and
run the cells top to bottom. Useful for testing prompts, inspecting the
scraped content, or tweaking the brochure tone.

### Option B — Run the web app

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser, enter a company name
and URL, and click **Generate**.

---

## Core functions (`brochure_logic.py`)

| Function | Purpose |
|---|---|
| `select_relevant_links(url)` | Asks Gemini to pick the most relevant links from the homepage, returns parsed JSON |
| `fetch_page_and_all_relevant_links(url)` | Scrapes the homepage + all relevant pages, combines into one text block |
| `create_brochure(company_name, url)` | Runs the full pipeline and returns the finished brochure as markdown |

`create_brochure()` **returns** the markdown string (rather than displaying
it directly) so it can be used by both the notebook and the Flask app.

---

## Notes

- Page content is truncated to keep prompts within a reasonable size —
  5,000 characters for the final brochure prompt.
- The model can be swapped by changing the `MODEL` variable — Gemini's
  Flash-tier models (fast and cheap) are a good fit for both steps of this
  pipeline.
- This is a personal/learning project — the Flask dev server (`app.run()`)
  is not intended for production deployment.

---

## Security

Never commit your `.env` file or paste your API key directly into code.
`.gitignore` already excludes `.env` in this repo. If a key is ever
accidentally exposed, regenerate it immediately from Google AI Studio —
the old one stops working the moment you do.
