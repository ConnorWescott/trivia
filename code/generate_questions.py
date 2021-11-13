from dataclasses import dataclass
from pathlib import Path
import random
import requests
import io
import os


@dataclass
class Topic:
    question: str
    answer: str


if __name__ == '__main__':
    parent_dir = Path(os.getcwd()).parent
    print(parent_dir)
    Qs = parent_dir.as_posix() + r"/data/Questions69.txt"
    As = parent_dir.as_posix() + r"/data/Answers69.txt"
    topic_list = list()

    for x in range(10):
        json = requests.get("https://api.urbandictionary.com/v0/random").json()

        for word in json.get("list"):
            question = word.get("word")
            answer = word.get("definition").replace("\n", " ")
            answer = answer.replace("\r", " ")
            answer = answer.replace("[", "")
            answer = answer.replace("]", "")
            if len(answer) > 150:
                continue
            topic = Topic(question=f"Please define: {question}", answer=answer)
            topic_list.append(topic)

    print(topic_list)
    counter = 1
    with open(As, 'w', encoding='utf-8') as answer_file:
        with open(Qs, 'w', encoding='utf-8') as question_file:
            for topic in topic_list:
                question_file.write(f"{counter}. {topic.question}{os.linesep}")
                answer_file.write(f"{counter}. {topic.answer}{os.linesep}")
                counter += 1
