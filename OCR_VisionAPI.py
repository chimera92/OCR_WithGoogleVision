import re
import requests
import base64
import os
import sys

API_KEY = "Your API Key Goes Here"


def getTextFromImage(sourcePath):
    with open(sourcePath, "rb") as image_file:
        data = """{
        "requests": [{
            "image": {
                    "content": "%s"

            },
            "features": [{
                "type": "TEXT_DETECTION",
                "maxResults": 1
            }]
        }]
    }""" % base64.b64encode(image_file.read())
        response = requests.post(url='https://vision.googleapis.com/v1/images:annotate?key={}'.format(API_KEY),
                                 data=data,
                                 headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return response.content
        else:
            print("Error!!\n" + response.content)
            return None


class MyException(Exception):
    pass


def writeStringToFile(response, outPath):
    with open(outPath, "w") as op:
        op.write(response)


def main():
    if (len(sys.argv) < 2):
        raise MyException("Pass Source DIR as command line ARG!!")

    sourceDirPath = sys.argv[1]

    for file in os.listdir(sourceDirPath):
        if not re.match(r'^.*?(\.png|\.jpeg|\.mpeg|\.jpg)$', file.lower()):
            continue
        sourcePath = os.path.join(sourceDirPath, file)
        if os.path.isfile(sourcePath):
            outPath = sourcePath + ".txt"
            if os.path.exists(outPath):
                print("{} : File already exists!!").format(outPath)
                continue
            response = getTextFromImage(sourcePath)
            writeStringToFile(response, outPath)


if __name__ == '__main__':
    main()
