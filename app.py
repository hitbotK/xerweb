from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid

app = Flask(__name__, template_folder='templates')  # ไปโฟลเดอร์ templates

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        filename = f"{uuid.uuid4()}.mp4"

        ydl_opts = {
            'outtmpl': filename,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return send_file(filename, as_attachment=True)

        except Exception as e:
            return render_template("index.html", message=f"❌ ผิดพลาด: {e}")

        finally:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except:
                    pass

    return render_template("index.html", message=None)

if __name__ == '__main__':
    app.run(debug=True)
