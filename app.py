import pdb
import json
import sys
import requests as r

sound_url = "https://api.soundoftext.com/sounds/"

def get_word_payload(word):
    payload = {
        "engine":"Google",
        "data":{
            "text":word,
            "voice":"en-US"
        }
    }
    return payload


def get_sound_word(word):
    print("Getting the word %s" %(word))
    payload = get_word_payload(word)
    headers = { "content-type":"application/json"}
    response = r.post(sound_url, json.dumps(payload), headers=headers)
    json_data = response.json()
    if json_data["success"]:
        response = r.get(sound_url + json_data["id"], headers=headers)
        json_data = response.json()
        return { "filename": json_data["location"], "word":word }

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
        for index, word in enumerate(words):
            data = get_sound_word(word)
            words_template += template.format(index=index, word=word, filename=data["filename"])

    with open("index.html", "r") as f:
        with open(output, "w") as out:
            template = f.read()
            out.write(template.format(script=template_js, words= words_template))