import json


def remove_duplicate_answers(data_name):
    """
    TODO @MaticSincek Please add basic docs.
    
    :param data_name: 
    :return: 
    """
    with open(f'../../data/{data_name}-v2.0_SL.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
        for item in data:

            for p in item['paragraphs']:

                for qa in p['qas']:
                    seen_answers = []
                    answers_json = []

                    for a in qa['answers']:
                        if a['text'] not in seen_answers:
                            seen_answers.append(a['text'])
                            answers_json.append(a)

                    qa['answers'] = answers_json

    with open(f'../../data/{data_name}-v2.0_SL_removed_duplicates.json', 'w', encoding='UTF-8') as file:
        json.dump(data, file)


if __name__ == '__main__':
    remove_duplicate_answers('train')
