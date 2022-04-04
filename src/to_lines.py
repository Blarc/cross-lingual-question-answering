import json


def print_paragraph(paragraph_, file_):
    print(paragraph_['context'], file=file_)
    for qas in paragraph_['qas']:
        for answer in qas['answers']:
            print(answer['text'], file=file_)

        print(qas['question'], file=file_)


if __name__ == '__main__':
    with open('../data/normans.json', 'r') as file:
        data = json.load(file)

    with open('../data/normans_lines.txt', 'w', encoding='UTF-8') as file:
        for paragraph in data['paragraphs']:
            print_paragraph(paragraph, file)
