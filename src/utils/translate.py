import json


def translate(data_name, number_of_parts):
    """
    Translates the json data with the help of the translated lines.
    The function expects files with translated lines to exist in the
    data directory.
    
    :param data_name: name of the data file (train, dev)
    :param number_of_parts: number of files the lines are going to be split to
    """
    with open(f'../../data/{data_name}-v2.0.json', 'r') as file:
        data = json.load(file)['data']
    translated_lines = []
    for part in range(number_of_parts):
        with open(f'../../data/tmp/{data_name}_SL/lines_{data_name}_part_{part}_SL.txt', 'r', encoding='UTF-8') as part_file:
            translated_lines.extend(part_file.readlines())
            
    index = 0
    for theme in data:
        for paragraph in theme['paragraphs']:
            paragraph['context'] = translated_lines[index].rstrip()
            index += 1
            for qas in paragraph['qas']:
                for answer in qas['answers']:
                    answer['text'] = translated_lines[index].rstrip()
                    index += 1
                if 'plausible_answers' in qas:
                    for plausible_answer in qas['plausible_answers']:
                        plausible_answer['text'] = translated_lines[index].rstrip()
                        index += 1

                qas['question'] = translated_lines[index].rstrip()
                index += 1
                
    with open(f'../../data/{data_name}-v2.0_SL.json', 'w', encoding='UTF-8') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    translate('train', 5)
