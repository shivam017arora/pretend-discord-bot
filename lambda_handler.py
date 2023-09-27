import boto3
import json


def get_voices(event, bs):
    import requests

    url = "https://api.elevenlabs.io/v1/voices"

    headers = {
        "Accept": "application/json",
        "xi-api-key": "4041172328f2929f0137c762bf7a4c2e",
    }

    response = requests.get(url, headers=headers)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, authorizationToken",
        },
        "body": response.text,
    }


def get_voice_from_text(voice_id, prompt):
    import requests

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "4041172328f2929f0137c762bf7a4c2e",
    }

    data = {
        "text": prompt,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    response = requests.post(url, json=data, headers=headers)
    with open(f"{prompt}.mp3", "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    return response
    # return {
    #     "statusCode": 200,
    #     "headers": {
    #         "Content-Type": "application/json",
    #         "Access-Control-Allow-Origin": "*",
    #         "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    #         "Access-Control-Allow-Headers": "Content-Type, authorizationToken",
    #     },
    #     "body": json.dumps(response),
    # }


if __name__ == "__main__":
    print(get_voices(None, None))
    # get_voice_from_text(
    #     {
    #         "voice_id": "zcAOhNBS3c14rBihAFp1",
    #         "prompt": "Welcome to THE world of REAL Voice N F Ts",
    #     },
    #     None,
    # )
