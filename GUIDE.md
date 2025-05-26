# Lichtblick App: Debugging & Troubleshooting Guide

This document outlines key issues encountered while deploying the Lichtblick German learning assistant, and how we resolved them. It serves as a practical reference for debugging Python/Streamlit apps, especially when deploying on Hugging Face Spaces.

---

## ✅ Environment Setup

### Issue:

`ValueError: <Token ...> was created in a different Context`

### Solution:

* This was caused by mixing `async` execution and Streamlit’s sync context. We fixed it by:

  * Making sure `trace(...)` calls were used **inside** Streamlit `with` blocks.
  * Refactoring `llm_response` to yield deltas without accumulating and re-yielding old text.

---

## ✅ OpenAI API Key Errors

### Issue:

`OpenAIError: The api_key client option must be set...`

### Solution:

* Ensured `OPENAI_API_KEY` was correctly loaded using `dotenv_values`.
* Later switched to **passing the API key manually** via Streamlit sidebar input for Hugging Face compatibility.

---

## ✅ Streamlit Streaming Glitches

### Issue:

Streamed text would repeat or show progressively longer output blocks.

### Solution:

* Refactored `llm_response()` to yield **only the latest delta** instead of the full accumulated string.
* Let Streamlit’s `st.write_stream()` handle the progressive display cleanly.

---

## ✅ Context Awareness

### Issue:

The agent didn’t understand follow-up questions.

### Solution:

* Built a context string from `st.session_state.messages[-4:]`.
* Clearly separated user/assistant turns using double newlines for clarity.
* Appended the current message at the end before passing it to the agent.

---

## ✅ Module Import Errors

### Issue:

`ModuleNotFoundError: No module named 'backend'`

### Solution:

We considered 3 options:

1. `sys.path.append(...)` — ✅ Initially used
2. `WORKDIR /app/src` in Dockerfile — ✅ Ultimately chosen
3. Creating a package via `setup.py` — ❌ Not used

We refactored to a flat layout and used:

```dockerfile
WORKDIR /app
COPY . .
ENTRYPOINT ["streamlit", "run", "app.py", ...]
```

---

## ✅ Hugging Face Build Errors

### Issue:

```
ERROR: file:///C:/Users/... does not appear to be a Python project
```

### Solution:

* Removed problematic local `-e file:///...` line from `requirements.txt`.
* Cleaned up `requirements.txt` to contain only valid packages like:

  ```
  streamlit
  openai
  python-dotenv
  ```

---

## ✅ Final Hugging Face Deployment Structure

```
/ (repo root)
├── app.py               # Streamlit app
├── lichtblick.py        # Agent logic
├── requirements.txt     # Clean, flat dependencies
├── Dockerfile           # WORKDIR /app
├── README.md            # App overview
└── assets/              # Mascot image, etc.
```

Let me know if you'd like to add sections about:

* Dev vs Prod Dockerfile differences

* Streamlit debugging in dev vs deployed

* Version control habits are critical to keeping your repo clean, collaborative, and deployable. Here are the key practices we followed for Lichtblick:

* Add `.venv/`, `.env`, `__pycache__/`, and `.egg-info/` to `.gitignore` to avoid committing virtual environments or temporary files.

* Do **not** version control `requirements.txt` generated with local paths (like `file:///...`). Use clean, portable package listings.