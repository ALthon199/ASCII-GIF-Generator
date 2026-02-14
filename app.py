import os
import io
import requests
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
from PIL import Image, ImageSequence
from dotenv import load_dotenv  

app = Flask(__name__)
CORS(app)
load_dotenv("secrets.txt")  # Load environment variables from secrets.txt
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
STANDARD_CHARS = list('@%#*+=-:. ')
BINARY_CHARS = list('01')
BLOCKS_CHARS = list('█▓▒░ ')
ASCII_CHARSETS = {
    'standard': STANDARD_CHARS,
    'binary': BINARY_CHARS,
    'blocks': BLOCKS_CHARS
}


def search_giphy(query):
    api_key = os.environ.get('GIPHY_API_KEY')
    if not api_key:
        return None
    url = f"https://api.giphy.com/v1/gifs/search"
    params = {
        'api_key': api_key,
        'q': query,
        'limit': 1,
        'rating': 'g'
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data['data']:
            return data['data'][0]['images']['original']['url']
    return None


def gif_to_ascii_stream(gif_bytes, width=120, ascii_chars=STANDARD_CHARS):
    n_chars = len(ascii_chars)
    with Image.open(io.BytesIO(gif_bytes)) as im:
        for frame in ImageSequence.Iterator(im):
            frame = frame.convert('L')
            wpercent = (width/float(frame.size[0]))
            hsize = int((float(frame.size[1])*float(wpercent)*0.55))  # Fix aspect ratio for ASCII
            frame = frame.resize((width, hsize))
            pixels = frame.getdata()
            ascii_str = "".join([
                ascii_chars[min(p // max(1, (256 // n_chars)), n_chars - 1)] for p in pixels
            ])
            ascii_img = "\n".join([ascii_str[i:i+width] for i in range(0, len(ascii_str), width)])
            yield f"data: {ascii_img}\n---END---\n"

@app.route('/stream', methods=['GET', 'POST'])
def stream_ascii():
    if request.method == 'POST':
        if not request.is_json:
            return Response('Request must be JSON.', status=400)
        prompt = request.json.get('prompt')
    else:
        prompt = request.args.get('prompt')
    if not prompt:
        return Response('Prompt required.', status=400)
    # If prompt looks like a URL, use it directly
    if isinstance(prompt, str) and (prompt.startswith('http://') or prompt.startswith('https://')):
        gif_url = prompt
    else:
        gif_url = search_giphy(prompt)
        if not gif_url:
            return Response('No GIF found.', status=404)
    gif_resp = requests.get(gif_url)
    if gif_resp.status_code != 200:
        return Response('Failed to download GIF.', status=502)

    invert = request.args.get('invert', 'false').lower() == 'true'
    charset = request.args.get('charset', 'standard').lower()
    ascii_chars = ASCII_CHARSETS.get(charset, STANDARD_CHARS)
    if invert:
        ascii_chars = ascii_chars[::-1]

    def generate():
        yield from gif_to_ascii_stream(gif_resp.content, width=120, ascii_chars=ascii_chars)

    headers = {'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
    return Response(stream_with_context(generate()), headers=headers)

@app.route('/gif_url')
def gif_url():
    prompt = request.args.get('prompt', '')
    gif_url = search_giphy(prompt)
    if not gif_url:
        return {'url': None}, 404
    return {'url': gif_url}

@app.route('/gif_list')
def gif_list():
    prompt = request.args.get('prompt', '')
    api_key = os.environ.get('GIPHY_API_KEY')
    if not api_key:
        return {'gifs': []}, 400
    url = f"https://api.giphy.com/v1/gifs/search"
    params = {
        'api_key': api_key,
        'q': prompt,
        'limit': 8,
        'rating': 'g'
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        gifs = [item['images']['original']['url'] for item in data.get('data', [])]
        return {'gifs': gifs}
    return {'gifs': []}, 502

@app.route('/')
def index():
    return 'ASCII GIF Generator Backend Running.'


# For local development only:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
