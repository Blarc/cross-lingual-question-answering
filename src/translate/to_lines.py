import json


def translate(data_name, number_of_parts):
    """
    Translates the json data with the help of the translated lines.
    The function expects files with translated lines to exist in the
    data directory.
    
    :param data_name: name of the data file (train, dev)
    :param number_of_parts: number of files the translated lines are split to
    """
    with open(f'../../data/{data_name}-v2.0.json', 'r') as file:
        data = json.load(file)['data']
    part_size = len(data) // number_of_parts + 1
    for part in range(number_of_parts):
        with open(f'../../data/tmp/lines_{data_name}_part_{part}.txt', 'w', encoding='UTF-8') as part_file:

            for theme in range(part * part_size, min((part + 1) * part_size, len(data))):

                for paragraph in data[theme]['paragraphs']:
                    print(paragraph['context'], file=part_file)
                    for qas in paragraph['qas']:
                        for answer in qas['answers']:
                            print(answer['text'], file=part_file)

                        print(qas['question'], file=part_file)


if __name__ == '__main__':
    translate('train', 2)
