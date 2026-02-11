# Streaming ASCII GIF Generator

## Overview

This project streams ASCII art versions of GIFs from Giphy (or Tenor) to the frontend using Server-Sent Events (SSE).

## Features

- User enters a prompt (e.g., 'cat')
- Backend searches Giphy (or Tenor as backup)
- Downloads GIF, converts frames to ASCII art
- Streams ASCII frames to frontend in real time

## Tech Stack

- Python (Flask)
- requests
- Pillow (PIL)
- flask-cors

## Setup

1. **Clone the repo**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables:**
   - For Giphy: `GIPHY_API_KEY`
   - For Tenor: `TENOR_API_KEY`
   - Example (Windows):
     ```powershell
     $env:GIPHY_API_KEY="your_giphy_key"
     $env:TENOR_API_KEY="your_tenor_key"
     ```
   - Example (Linux/macOS):
     ```bash
     export GIPHY_API_KEY=your_giphy_key
     export TENOR_API_KEY=your_tenor_key
     ```

4. **Run the backend:**

   ```bash
   python app.py
   ```

5. **Open `index.html` in your browser.**
   - Or deploy both files to Render and set environment variables in Render's dashboard.

## Notes

- API keys are NOT hardcoded. Set them as environment variables.
- SSE streaming uses `stream_with_context` and disables buffering with `X-Accel-Buffering: no`.
- If Giphy fails, Tenor is used as backup.

## Troubleshooting

- If you get 406 errors on Render, make sure `X-Accel-Buffering: no` is set in response headers.
- If GIFs don't appear, check your API keys and internet connection.

## License

MIT
