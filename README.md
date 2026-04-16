# Day-11-Guardrails-HITL-Responsible-AI

Day 11 — Guardrails, HITL & Responsible AI: How to make agent applications safe?

## Objectives

- Understand why guardrails are mandatory for AI products
- Implement input guardrails (injection detection, topic filter)
- Implement output guardrails (content filter, LLM-as-Judge)
- Use NeMo Guardrails (NVIDIA) with Colang
- Design HITL workflow with confidence-based routing
- Perform basic red teaming

## Project Structure

```
Day-11-Guardrails-HITL-Responsible-AI/
├── notebooks/
│   ├── lab11_guardrails_hitl.ipynb            # Student lab (Colab)
│   └── lab11_guardrails_hitl_solution.ipynb   # Solution (instructor only)
├── src/                                       # Local Python version
│   ├── main.py                    # Entry point — run all parts or pick one
│   ├── core/
│   │   ├── config.py              # API key setup, allowed/blocked topics
│   │   └── utils.py               # chat_with_agent() helper
│   ├── agents/
│   │   └── agent.py               # Unsafe & protected agent creation
│   ├── attacks/
│   │   └── attacks.py             # TODO 1-2: Adversarial prompts & AI red teaming
│   ├── guardrails/
│   │   ├── input_guardrails.py    # TODO 3-5: Injection detection, topic filter, plugin
│   │   ├── output_guardrails.py   # TODO 6-8: Content filter, LLM-as-Judge, plugin
│   │   └── nemo_guardrails.py     # TODO 9: NeMo Guardrails with Colang
│   ├── testing/
│   │   └── testing.py             # TODO 10-11: Before/after comparison, pipeline
│   └── hitl/
│       └── hitl.py                # TODO 12-13: Confidence router, HITL design
├── requirements.txt
└── README.md
```

## Setup

### Google Colab (recommended)

1. Upload `notebooks/lab11_guardrails_hitl.ipynb` to Google Colab
2. Create a Google API Key at [Google AI Studio](https://aistudio.google.com/apikey)
3. Save the API key in Colab Secrets as `GOOGLE_API_KEY`
4. Run cells in order

### Local (Notebook)

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export GOOGLE_API_KEY="your-api-key-here"   # or create a .env file (see .env.example)
jupyter notebook notebooks/lab11_guardrails_hitl.ipynb
```

### Local (Python modules — no Colab needed)

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export GOOGLE_API_KEY="your-api-key-here"   # or create a .env file (see .env.example)

# Run the full lab
cd src/
python main.py

# Or run specific parts
python main.py --part 1    # Part 1: Attacks
python main.py --part 2    # Part 2: Guardrails
python main.py --part 3    # Part 3: Testing pipeline
python main.py --part 4    # Part 4: HITL design

# Or test individual modules
python guardrails/input_guardrails.py
python guardrails/output_guardrails.py
python testing/testing.py
python hitl/hitl.py
```

### Tools Used

- **Google ADK** — Agent Development Kit (plugins, runners)
- **NeMo Guardrails** — NVIDIA framework with Colang (declarative safety rules)
- **Gemini 2.5 Flash/Flash Lite** — LLM backend (you can switch to other models if you want)

## Lab Structure (2.5 hours)

| Part | Content | Duration |
|------|---------|----------|
| Part 1 | Attack unprotected agent + AI red teaming | 30 min |
| Part 2A | Implement input guardrails (injection, topic filter) | 20 min |
| Part 2B | Implement output guardrails (content filter, LLM-as-Judge) | 20 min |
| Part 2C | NeMo Guardrails with Colang (NVIDIA) | 20 min |
| Part 3 | Before/after comparison + automated testing pipeline | 30 min |
| Part 4 | Design HITL workflow | 30 min |

## Deliverables

1. **Security Report**: Before/after comparison of 5+ attacks (ADK + NeMo)
2. **HITL Flowchart**: 3 decision points with escalation paths

## 13 TODOs

| # | Description | Framework |
|---|-------------|-----------|
| 1 | Write 5 adversarial prompts | - |
| 2 | Generate attack test cases with AI | Gemini |
| 3 | Injection detection (regex) | Python |
| 4 | Topic filter | Python |
| 5 | Input Guardrail Plugin | Google ADK |
| 6 | Content filter (PII, secrets) | Python |
| 7 | LLM-as-Judge safety check | Gemini |
| 8 | Output Guardrail Plugin | Google ADK |
| 9 | NeMo Guardrails Colang config | NeMo |
| 10 | Rerun 5 attacks with guardrails | Google ADK |
| 11 | Automated security testing pipeline | Python |
| 12 | Confidence Router (HITL) | Python |
| 13 | Design 3 HITL decision points | Design |

## References

- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Official Google's Gemini cookbook](https://github.com/google-gemini/cookbook/blob/main/examples/gemini_google_adk_model_guardrails.ipynb)
- [AI Safety Fundamentals](https://aisafetyfundamentals.com/)
- [AI Red Teaming Guide](https://github.com/requie/AI-Red-Teaming-Guide)
- [antoan.ai - AI Safety Vietnam](https://antoan.ai)
