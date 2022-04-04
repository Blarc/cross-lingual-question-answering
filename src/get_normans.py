import json

if __name__ == '__main__':
    with open('../data/dev-v2.0.json', 'r') as file:
        data = json.load(file)['data']

    with open('../data/normans.json', 'w') as normans_file:
        json.dump(data[0], normans_file, sort_keys=True, indent=4)

    with open('../data/normans_one.json', 'w') as normans_file:
        json.dump(data[0]['paragraphs'][0], normans_file, sort_keys=True, indent=4)
