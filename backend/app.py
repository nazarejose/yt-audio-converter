from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
from pytubefix import YouTube
import os
import subprocess
from tempfile import NamedTemporaryFile

app = Flask(__name__)
CORS(app)

@app.route('/api/download-audio', methods=['POST'])
def download_audio():
    @after_this_request
    def add_headers(response):
        response.headers.add('Access-Control-Expose-Headers', 'Content-Disposition')
        return response
    
    data = request.json
    youtube_link = data.get('link')
    
    if not youtube_link:
        return jsonify({"error": "No link provided"}), 400

    try:
        youtube_video = YouTube(youtube_link)
        title = youtube_video.title
        audio_stream = youtube_video.streams.filter(only_audio=True).first()

        with NamedTemporaryFile(delete=False, suffix='.webm') as temp_audio_file:
            audio_file = audio_stream.download(filename=temp_audio_file.name)

        with NamedTemporaryFile(delete=False, suffix='.mp3') as temp_mp3_file:
            output_file = temp_mp3_file.name
            command = f'ffmpeg -y -i "{audio_file}" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "{output_file}"'
            subprocess.run(command, shell=True, check=True)

            os.remove(audio_file)

            response = send_file(
                output_file,
                as_attachment=True,
                download_name=f"{title}.mp3",
                mimetype="audio/mp3"
            )
            response.headers['Content-Disposition'] = f'attachment; filename="{title}.mp3"'
            return response

    except Exception as e:
        return jsonify({"error": f"Failed to download and convert audio: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
