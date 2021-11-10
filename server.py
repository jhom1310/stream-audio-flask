from flask import Flask, Response, jsonify
from flask import after_this_request
from pytube import YouTube, Playlist
import time


app = Flask(__name__)

""" @app.route("/1")
def stream1():
    VIDEO_URL = 'https://www.youtube.com/watch?v=VxOU7rr8Xjc&ab_channel=AleffJonathan'
    yt = YouTube(VIDEO_URL)
    audio = yt.streams.filter(only_audio=True)[0]
    audio.download()
    def generate():         
        with open('{}.mp4'.format(audio.title), "rb") as fmp4:
            data = fmp4.read(1024)
            while data:
                yield data
                data = fmp4.read(1024)
    return Response(generate(), mimetype="audio/mp4")

@app.route("/2")
def stream2():
    VIDEO_URL = 'https://www.youtube.com/watch?v=QuKTH18OBII&ab_channel=ORappa'
    yt = YouTube(VIDEO_URL)
    audio = yt.streams.filter(only_audio=True)[0]
    audio.download()
    def generate():         
        with open('{}.mp4'.format(audio.title), "rb") as fmp4:
            data = fmp4.read(1024)
            while data:
                yield data
                data = fmp4.read(1024)
    return Response(generate(), mimetype="audio/mp4") """
        

PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PL0y4Kqm8ayHTeNwNnrZDxpRZlp-QVSY1_'
playlist = Playlist(PLAYLIST_URL)
count = 0
for url in playlist:
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True)[0]
    audio.download()
    exec(
    '''
@app.route("/{}")
def stream{}():
    def generate():       
        with open('{}.mp4', "rb") as fmp4:
            data = fmp4.read(1024)
            while data:
                yield data
                data = fmp4.read(1024)
    return Response(generate(), mimetype="audio/mp4")
        '''.format(count, count, audio.title), globals()
   )
    count += 1
    
@app.route('/hello')
def hello():
    return jsonify({'qtd': count})

if __name__ == "__main__":
    app.run(debug=True)