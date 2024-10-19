from pytube import YouTube


def download_video(url, output_path):
    try:
        yt = YouTube(url)

        stream = yt.streams.get_highest_resolution()

        # Download the video
        stream.download(output_path)
        print("Video downloaded successfully!")

    except Exception as e:
        print("Error:", e)


video_url = "https://youtu.be/ENLEjGozrio?si=4js1YHGVwMj1sw-Z"
output_path = "home/ebuka"

download_video(video_url, output_path)
