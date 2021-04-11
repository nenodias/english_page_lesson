import pdb
import json
import sys
import aiohttp
import asyncio

sound_url = "https://api.soundoftext.com/sounds/"


def get_word_payload(word):
    payload = {
        "engine": "Google",
        "data": {
            "text": word,
            "voice": "en-US"
        }
    }
    return payload


async def get_sound_word(r, word):
    print("Getting the word %s" % (word))
    payload = get_word_payload(word)
    headers = {"content-type": "application/json"}
    response = await r.post(sound_url, json=payload)
    json_data = await response.json()
    if json_data["success"]:
        response = await r.get(sound_url + json_data["id"])
        json_data = await response.json()
        return {"filename": json_data["location"], "word": word}
    return {"filename": None, "word": word}


async def get_words(r, words):
    futures = []
    for word in words:
        futures.append(loop.create_task(get_sound_word(r, word)))
    return await asyncio.gather(*futures)


async def main():
    async with aiohttp.ClientSession() as session:
        template = ""

        with open("template.html", "r") as f:
            template = f.read()

        template_js = ""

        with open("template.js", "r") as f:
            template_js = f.read()

        words_template = ""

        if len(sys.argv) > 1:
            filename = sys.argv[1]
            output = filename.replace(".txt", ".html")

            with open(filename, "r") as f:
                words = f.read().split("\n")
                words_template = ""
                generator = await get_words(session, words)
                for index, data in enumerate(generator):
                    word = data["word"]
                    words_template += template.format(
                        index=index, word=word, filename=data["filename"])

            with open("index.html", "r") as f:
                with open(output, "w") as out:
                    template = f.read()
                    out.write(template.format(
                        script=template_js, words=words_template))


loop = asyncio.get_event_loop()
tasks = [main()]
loop.run_until_complete(asyncio.wait(tasks))
