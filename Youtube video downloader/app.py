from flask import Flask,request,redirect,render_template
import pytube 
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.errorhandler(404)
def notFound(err):
    return render_template("404.html"),404

@app.route("/download", methods=["POST"])
def getLinks():
    try:
        ytUrl = request.form['video_url']
        yt = pytube.YouTube(ytUrl)
        streams = [yt.streams.get_lowest_resolution(), yt.streams.get_highest_resolution(), yt.streams.get_audio_only()]
        for stream in streams:
            stream.download(f"static/videos/",filename=f"{yt.title}{streams.index(stream)}.mp4")

        videos = os.listdir("static/videos")
        videos = [os.path.join("static/videos/",i) for i in videos]
        return render_template("downloadlinks.html", videos=videos, title=yt.title)
    except Exception as e:
        print(e)
        return "<script>alert('Invalid link, enter again!');window.location.href='/';</script>"

if __name__ == "__main__":
    app.run()
