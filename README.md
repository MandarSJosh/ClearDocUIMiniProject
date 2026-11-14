# ClearDoc: Local Plain-Language Assistant

ClearDoc is an on-device, privacy-first Human-Computer Interaction (HCI) prototype designed to simplify dense medical and legal text for elderly users without relying on cloud APIs.

## Project Structure
* `app.py`: Main Streamlit application with local Ollama integration and human-in-the-loop review gate.
* `requirements.txt`: Pinned Python dependencies.
* `sample_inputs/`: Folder containing test texts (Warfarin medical label, Terms of Service, Cloud SLA).

---

## Setup & Reproduction Instructions

### Step 1: Prerequisites
1. Ensure **Python 3.10+** is installed on your system.
2. Download, install, and run **Ollama** from [ollama.com](https://ollama.com).

### Step 2: Download the Local Model
Open your terminal and pull the mandatory local model:
```bash
ollama pull gemma4:e2b