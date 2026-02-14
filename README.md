## Backend API Endpoints

### `/stream` (GET/POST)

- Streams ASCII art frames from a GIF.
- **Parameters:**
  - `prompt` (string, required): Search term or direct GIF URL (POST JSON or GET query)
  - `invert` (bool, optional): Invert ASCII charset (default: false)
  - `charset` (string, optional): ASCII charset to use (`standard`, `binary`, `blocks`; default: `standard`)
- **Returns:**
  - `text/event-stream` with ASCII art frames, separated by `---END---`.

These results are not cached, every stream will refetch the gif_url even if its the same.
For example, selecting a filter will refetch the url with the parameter

### `/gif_url` (GET)

- Returns a single GIF URL for a search prompt.
- **Parameters:**
  - `prompt` (string, required): Search term.
- **Returns:**
  - `{ "url": <gif_url> }` or 404 if not found.

### `/gif_list` (GET)

- Returns a list of GIF URLs for a search prompt.
- **Parameters:**
  - `prompt` (string, required): Search term.
- **Returns:**
  - `{ "gifs": [<gif_url>, ...] }` or 400/502 on error.

### `/` (GET)

- Health check endpoint. Returns a simple status message.

## Frontend Communication

- The frontend calls `/gif_list` to search for GIFs and display thumbnails.
- When a GIF is selected, the frontend calls `/stream` (POST) with the GIF URL to receive a stream of ASCII art frames for display.
- The frontend may also call `/gif_url` for a single GIF result.

## Environment Variables & Secrets

- The backend loads secrets from `secrets.txt` (locally) or environment variables (in production, e.g., Render dashboard).
- **API keys and secrets are never exposed to the frontend or committed to version control.**
- The `.gitignore` file ensures `secrets.txt` is not tracked.

## Authentication & Security
- No user authentication is implemented (public API for demo purposes).
- All API keys (e.g., GIPHY) are stored securely on the backend and never sent to the frontend.

---





