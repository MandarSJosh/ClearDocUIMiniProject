# ClearDoc: Privacy-First Local Medical & Legal Text Simplifier

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)

**ClearDoc** is an on-device, privacy-first desktop web application designed to help older adults and non-experts safely simplify dense, jargon-heavy clinical labels, FDA drug instructions, and legal terms of service. Built for SUTD 50.006 User Interface Design and Implementation.

---

## Key Features
* **100% Local & Private:** Operates entirely on-device via Ollama (`gemma4:e2b`), ensuring sensitive health data never leaves your machine or touches external cloud APIs.
* **Human-in-the-Loop Review Gate:** Because small local models are prone to hallucinations or clinical oversimplifications, ClearDoc forces a side-by-side comparison. Users or caregivers must manually review the draft and tick a mandatory verification checklist before unlocking export/download options.
* **Built-In Test Suite:** Includes an integrated test-case selector allowing markers and users to instantly load standardized test inputs (Rheumatoid Arthritis, OpenAI Terms of Service, and Warfarin Clinical Label).
* **Controlled Generation:** Configured with low temperature (`0.1`) and structured streaming status indicators to maximize output consistency and user feedback during local inference.

---

## System Architecture & Tech Stack
* **Frontend UI:** Streamlit (`app.py`) providing a clean, high-contrast, responsive two-column layout.
* **Local Inference Engine:** Ollama running Gemma 4 (`gemma4:e2b`) locally via Apple Silicon hardware acceleration.
* **State Management:** Streamlit Session State (`is_approved`, `do_reset`) to manage review gates and reset flows cleanly.

---

## Clean-Run Installation & Setup Instructions

Follow these exact steps to run ClearDoc locally from scratch:

### Prerequisites
1. Ensure **Python 3.10 or later** is installed on your system.
2. Download and install [Ollama](https://ollama.com) and ensure the Ollama desktop service is running in your background tray.

### Step-by-Step Guide
1. **Pull the Local Model:**
   Open your terminal and download the required Gemma model:
   ```bash
   ollama pull gemma4:e2b