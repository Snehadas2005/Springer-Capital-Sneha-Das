# Compliance Document Review App — AI Track (`AI-2`)

An enterprise-grade **AI Compliance Inspection Agent** built with **FastAPI** and **Google Gemini 3.6 Flash**. This service evaluates financial and legal documents against regulatory compliance rules (e.g., SEC, FINRA) while enforcing strict anti-hallucination guardrails through verbatim substring verification and character offset extraction.

## 🌟 Key Features

- **Structured Compliance Inspection:** Evaluates raw document text against active rule sets defined in `rules.json`.
- **Zero-Hallucination Guardrail (Anti-Hallucination Substring Validator):** Post-processes all AI-generated flags to ensure cited passages exist _verbatim_ in the source text. Discards any hallucinated or modified quotes automatically.
- **Character-Level Offsets:** Computes exact `start` and `end` character indices for each verified violation flag to enable seamless UI highlight rendering.
- **FastAPI Interactive Documentation:** Auto-generated Swagger UI for testing API endpoints.
- **Automated Test Suite:** Built-in `pytest` coverage for validating substring matching and anti-hallucination behavior.

## 🏗️ Architecture & Data Flow

```

[ Incoming Request ]
│ (document_text)
▼
┌─────────────────────────────────────────────────────────┐
│ 1. LLM Inspection Agent (app/services/llm_agent.py)    │
│ • Evaluates text against active rules (data/rules.json) │
│ • Enforces Structured JSON Output via Gemini API       │
└─────────────────────────────────────────────────────────┘
│ (Raw Violation Flags)
▼
┌─────────────────────────────────────────────────────────┐
│ 2. Substring Validator (app/services/validator.py)     │
│ • Verifies verbatim match in source document            │
│ • Calculates character offsets: { start: 21, end: 105 } │
│ • Discards unmatched / hallucinated flags               │
└─────────────────────────────────────────────────────────┘
│ (Validated Flags + Offsets)
▼
[ API Response Payload ]

```

## 📁 Project Structure

```text
ai-inspection-service/
├── app/
│   ├── main.py              # FastAPI application & endpoint definitions
│   ├── models/
│   │   └── schemas.py       # Pydantic data models & request/response schemas
│   └── services/
│       ├── llm_agent.py     # Gemini API integration & structured output generation
│       └── validator.py     # Anti-hallucination verbatim matcher & offset calculator
├── data/
│   ├── rules.json           # Active compliance rules fixture
│   └── sample_doc.txt       # Sample document for testing
├── tests/
│   ├── conftest.py          # Pytest path configuration
│   └── test_validator.py    # Unit tests for validator and edge-case handling
├── .env                     # Environment variables (API keys - gitignored)
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation

```

## 🛠️ Prerequisites & Installation

### 1. Prerequisites

- **Python 3.10+** installed on your system.
- A **Google Gemini API Key** (Obtainable from [Google AI Studio](https://aistudio.google.com/?utm_source=gemini)).

### 2. Setup Environment

1. Clone the repository and navigate to the project directory:

```bash
cd ai-inspection-service

```

2. Create and activate a virtual environment:

- **Windows:**

```powershell
python -m venv .venv
.\.venv\Scripts\activate

```

- **macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate

```

3. Install required dependencies:

```bash
pip install -r requirements.txt

```

4. Create a `.env` file in the root directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here

```

## 🚀 Running the Application

Start the FastAPI development server using Uvicorn:

```bash
uvicorn app.main:app --reload

```

Once running, access the interactive API documentation at:

- **Swagger UI:** [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs&utm_source=gemini)
- **ReDoc:** [http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc&utm_source=gemini)

## 🧪 Testing API & Unit Tests

### 1. Testing `/inspect` Endpoint via cURL

```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/inspect](http://127.0.0.1:8000/inspect)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "document_text": "Welcome to our fund. We guarantee Jane Smith an 18% annual return on investment without any market risk."
}'

```

#### Example Output Response:

```json
{
  "status": "success",
  "flags": [
    {
      "rule_id": "FINRA-2210",
      "passage": "We guarantee Jane Smith an 18% annual return on investment without any market risk.",
      "reason": "Promising guaranteed returns or zero market risk is strictly prohibited under FINRA-2210.",
      "severity": "HIGH",
      "offsets": {
        "start": 21,
        "end": 105
      }
    }
  ]
}
```

### 2. Running Automated Unit Tests

Run the test suite using `pytest`:

```bash
python -m pytest tests/

```

Tests verify:

1. Valid verbatim passages correctly compute `start` and `end` character offsets.
2. Hallucinated or slightly altered passages generated by LLMs are automatically discarded.

## 📜 Active Rules Reference (`data/rules.json`)

- **`FINRA-2210`**: Prohibits promising guaranteed fixed returns or claims of zero market risk.
- **`SEC-ADV-2`**: Requires all performance claims to explicitly state that past performance does not guarantee future results.
