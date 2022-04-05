import json


def to_lines(data_name, number_of_parts):
    """
    Converts all json data, that needs to be translated to separate lines.
    These files with lines can be sent to eTranslation for translating.
    For keeping the files small enough, parameter :param number_of_parts
    can be specified.
    
    :param data_name: name of the data file (train, dev)
    :param number_of_parts: number of files the lines are going to be split to
    """
    with open(f'../../data/{data_name}-v2.0.json', 'r') as file:
        data = json.load(file)['data']
    translated_lines = []
    for part in range(number_of_parts):
        with open(f'../../data/tmp/lines_{data_name}_part_{part}_SL.txt', 'r', encoding='UTF-8') as part_file:
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

                qas['question'] = translated_lines[index].rstrip()
                index += 1
    with open(f'../../data/{data_name}-v2.0_SL.json', 'w', encoding='UTF-8') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    to_lines('dev', 1)
