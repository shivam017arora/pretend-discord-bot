import json
import asyncio
import requests


def download_video(video_url, save_path):
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    with open(save_path, "wb") as video_file:
        for chunk in response.iter_content(chunk_size=8192):
            video_file.write(chunk)


from moviepy.editor import VideoFileClip


def crop_video(video_path, output_path, crop_bottom=20):
    """
    Crop the video from the bottom by the specified amount.
    The crop_bottom parameter is in pixels.
    """
    with VideoFileClip(video_path) as clip:
        cropped_clip = clip.crop(y2=clip.size[1] - crop_bottom)  # crop from the bottom
        cropped_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")


async def generate_video():
    did_key = "c2hpdmFtYXR1Y3dAZ21haWwuY29t:0cWFt9EkSQ9O47aIDwfOB"

    url = "https://api.d-id.com/talks"

    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {"type": "elevenlabs", "voice_id": "piTKgcLEGmPE4e6mEKli"},
            "ssml": "false",
            "input": "Hello World"
        },
        "config": {"fluent": "false", "pad_audio": "0.0"},
        "source_url": "https://github.com/OpenTalker/SadTalker/blob/main/examples/source_image/art_0.png?raw=true",
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik53ek53TmV1R3ptcFZTQjNVZ0J4ZyJ9.eyJodHRwczovL2QtaWQuY29tL2ZlYXR1cmVzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jeF9sb2dpY19pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vY2hhdF9zdHJpcGVfc3Vic2NyaXB0aW9uX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfY3VzdG9tZXJfaWQiOiJjdXNfT2k2VjdrZ1BrWkpINU0iLCJpc3MiOiJodHRwczovL2F1dGguZC1pZC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDcyMDY4NTU1MDYwMTE0NTA0ODQiLCJhdWQiOlsiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTU3NTQwNjMsImV4cCI6MTY5NTg0MDQ2MywiYXpwIjoiR3pyTkkxT3JlOUZNM0VlRFJmM20zejNUU3cwSmxSWXEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIHJlYWQ6Y3VycmVudF91c2VyIHVwZGF0ZTpjdXJyZW50X3VzZXJfbWV0YWRhdGEgb2ZmbGluZV9hY2Nlc3MifQ.aV-yOzZAgz6r5FK0Su9d4l0Ughj8JzDbho8oGFNzz7NM56UR17RJgtW4eO9zFaWIJB_eNNaDah6DTJAtsGf8SFDmqUAPQzhB7-g8lcLwwsf8vP5QaMoNn71ij4Z_4bN7NkqzX9tnvc-XgMkuj43xij98B-U-eHz252SLjrgqoU0j_3uAsWijOsrj1-OI4F79GIvsSF8xmPGauiCiuI1wtAvNEV7kvTTHS7RUwoWoITR3nupp0FRSrIXiOeeCGE7WLRByAJeZfGdmvWa9J4j56_j4vP4EdcJBALyHIjEXwFv_YG8ElpdIJNyaoY_GK3o8jpDaA3AIdKbfs9ZZ3I9NeQ",
    }

    response_clip = requests.post(url, json=payload, headers=headers)
    print(response_clip.text, type(response_clip.text))

    while True:
        url = "https://api.d-id.com/talks/" + json.loads(response_clip.text).get("id")

        headers = {
            "accept": "application/json",
            "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik53ek53TmV1R3ptcFZTQjNVZ0J4ZyJ9.eyJodHRwczovL2QtaWQuY29tL2ZlYXR1cmVzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jeF9sb2dpY19pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vY2hhdF9zdHJpcGVfc3Vic2NyaXB0aW9uX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfY3VzdG9tZXJfaWQiOiJjdXNfT2k2VjdrZ1BrWkpINU0iLCJpc3MiOiJodHRwczovL2F1dGguZC1pZC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDcyMDY4NTU1MDYwMTE0NTA0ODQiLCJhdWQiOlsiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTU3NTQwNjMsImV4cCI6MTY5NTg0MDQ2MywiYXpwIjoiR3pyTkkxT3JlOUZNM0VlRFJmM20zejNUU3cwSmxSWXEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIHJlYWQ6Y3VycmVudF91c2VyIHVwZGF0ZTpjdXJyZW50X3VzZXJfbWV0YWRhdGEgb2ZmbGluZV9hY2Nlc3MifQ.aV-yOzZAgz6r5FK0Su9d4l0Ughj8JzDbho8oGFNzz7NM56UR17RJgtW4eO9zFaWIJB_eNNaDah6DTJAtsGf8SFDmqUAPQzhB7-g8lcLwwsf8vP5QaMoNn71ij4Z_4bN7NkqzX9tnvc-XgMkuj43xij98B-U-eHz252SLjrgqoU0j_3uAsWijOsrj1-OI4F79GIvsSF8xmPGauiCiuI1wtAvNEV7kvTTHS7RUwoWoITR3nupp0FRSrIXiOeeCGE7WLRByAJeZfGdmvWa9J4j56_j4vP4EdcJBALyHIjEXwFv_YG8ElpdIJNyaoY_GK3o8jpDaA3AIdKbfs9ZZ3I9NeQ",
        }

        response = requests.get(url, headers=headers)

        print(response.text)
        if json.loads(response.text).get("status") == "done":
            print(response.text, type(response.text))
            video_url = json.loads(response.text).get("result_url")
            download_video(video_url, "downloaded_video.mp4")
            crop_video(
                "downloaded_video.mp4", "cropped_video.mp4", crop_bottom=200
            )  # You'll need to
            break

        await asyncio.sleep(30)  # Sleep for 30 seconds before the next poll


if __name__ == "__main__":
    asyncio.run(generate_video())
    # crop_video("downloaded_video.mp4", "cropped_video.mp4", crop_bottom=100)  # You'll need to
