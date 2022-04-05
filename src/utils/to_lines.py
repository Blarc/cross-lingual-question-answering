import json


def to_lines(data_name, number_of_parts):
    """
    Converts all json data, that needs to be translated to separate lines.
    These files with lines can be sent to eTranslation for translating.
    For keeping the files small enough, parameter :param number_of_parts
    can be specified.
    
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
    to_lines('train', 5)
