# Captioning images with [Moondream](https://moondream.ai/docs) model from moondream.ai
#
# Richard Anton - https://github.com/ranton256

import sys

from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
import filetype
import os

model_id = "vikhyatk/moondream2"
revision = "2024-08-26"

example_image_urls = [
    "https://ranton-example-files.s3.us-west-2.amazonaws.com/reading.jpg",
    "https://ranton-example-files.s3.us-west-2.amazonaws.com/lighthouse.png",
    "https://ranton-example-files.s3.us-west-2.amazonaws.com/birds.jpg"
]


def download_file(url, filename):
    response = requests.get(url)
    with open(filename, mode="wb") as file:
        file.write(response.content)
    print(f"Downloaded {url} to file {filename}")


def get_example_images():
    image_files = []
    for idx, url in enumerate(example_image_urls):
        filename = f"image_{idx}"
        if not os.path.exists(filename):
            print(f"File {filename} not found, downloading from {url}")
            download_file(url, filename)

        print(os.stat(filename))
        kind = filetype.guess(filename)
        if kind is None:
            print('Cannot guess file type for', filename)
            continue

        print('File extension: %s' % kind.extension)
        print('File MIME type: %s' % kind.mime)
        newname = f"{filename}.{kind.extension}"
        os.rename(filename, newname)
        print(f"Renamed {filename} to {newname}")
        image_files.append(newname)
        return image_files


def process_image(model, tokenizer, filename):
    image = Image.open(filename)
    enc_image = model.encode_image(image)
    description = model.answer_question(enc_image, "Describe this image.", tokenizer)
    print(f"Image: {filename} --> {description}")


def main():
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, revision=revision)
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model.generation_config.pad_token_id = tokenizer.pad_token_id

    if len(sys.argv) > 0:
        image_files = sys.argv[1:]
    else:
        image_files = get_example_images()

    for image_filename in image_files:
        process_image(model, tokenizer, image_filename)


if __name__ == "__main__":
    main()
