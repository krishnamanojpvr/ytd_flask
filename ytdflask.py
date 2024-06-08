from fastapi import HTTPException
from pytube import YouTube
import flask_cors
from flask import Flask, send_file, request
import os
app = Flask(__name__)
flask_cors.CORS(app)

@app.get("/download")
async def download_video():
    try:
        # Create a YouTube object
        url = request.args.get("url")
        print(url)
        yt = YouTube(url)

        # Get the highest resolution video stream
        print(1)
        stream = yt.streams.get_highest_resolution()

        # Download the video to the current working directory
        print(2)
        videopath = stream.download()

        print(3)
        os.rename(videopath, "video.mp4")

        print(4)

        return {"message": "Video downloaded successfully"}
    
    except KeyError:
        raise HTTPException(
            status_code=400, detail="Error: Video is not available or cannot be downloaded")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Error downloading video: " + str(e))


@app.route("/video")
def stream_video():
    video_path = os.path.join(os.path.dirname(__file__), "video.mp4")
    file_size = os.path.getsize(video_path)
    # range_header = request.headers.get("Range", None)

    # if range_header:
    #     try:
    #         start, end = map(int, range_header.replace("bytes=", "").split("-"))
    #     except ValueError:
    #         start, end = 0, file_size - 1
    # else:
    start, end = 0, file_size - 1

    chunk_size = (end - start) + 1
    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": chunk_size,
        "Content-Type": "video/mp4"
    }

    response = send_file(video_path, mimetype="video/mp4")
    response.headers.extend(headers)
    response.status_code = 200
    # if range_header , then statuscode = 206
    return response


if __name__ == "__main__":
    app.run(debug=True)
