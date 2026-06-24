# Werewolf AI - Backend

This repository contains the backend for the Werewolf (Secret Mafia) game simulation using LLM agents via OpenRouter and the TextArena environment. The backend exposes an API built with FastAPI that sends game events in real-time through an SSE (Server-Sent Events) stream.

## Prerequisites

* Python 3.8 or newer.
* OpenRouter API key configured in `werwolf_main.py` (or set as the `OPENROUTER_API_KEY` environment variable).

## Installation

1. **Clone the repository** (if applicable) and navigate to the backend directory.
2. **Install the required dependencies**:
   It is recommended to use a virtual environment (`venv` or `conda`). Run the following command to install the necessary packages:

   ```bash
   pip install fastapi uvicorn textarena