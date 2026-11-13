# ClearDoc: Local Plain-Language Assistant

ClearDoc is an on-device, privacy-first Human-Computer Interaction (HCI) prototype designed to simplify dense medical and legal text for elderly users without relying on cloud APIs.

## Prerequisites
1. **Python 3.10+** installed on your system.
2. **Ollama** installed and running in the background (download from https://ollama.com).

## Step 1: Download the Local Model
Open your terminal and pull the required Gemma 4 (2B) model. This is mandatory as the app runs 100% locally:
```bash
ollama pull gemma4:e2b