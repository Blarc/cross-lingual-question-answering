import json


def translate_paragraph(paragraph_, translated_lines_, index_):
    paragraph_['context'] = translated_lines_[index_].rstrip()
    index_ += 1
    for qas in paragraph_['qas']:
        for answer in qas['answers']:
            answer['text'] = translated_lines_[index_].rstrip()
            index_ += 1

        qas['question'] = translated_lines_[index_].rstrip()
        index_ += 1
    
    return index_


if __name__ == '__main__':
    with open('../data/normans.json', 'r') as file:
        data = json.load(file)

    with open('../data/normans_lines_SL.txt', encoding='UTF-8') as translated_file:
        translated_lines = translated_file.readlines()
        
        index = 0
        for paragraph in data['paragraphs']:
            index = translate_paragraph(paragraph, translated_lines, index)

    with open('../data/normans_translated.json', 'w', encoding='UTF-8') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4, ensure_ascii=False)
