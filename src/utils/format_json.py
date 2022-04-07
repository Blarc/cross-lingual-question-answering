import json

if __name__ == '__main__':
    with open('../../data/dev-v2.0.json', 'r') as file:
        with open('../../data/dev-v2.0-formatted.json', 'w', encoding='UTF-8') as formatter_file:
            json.dump(json.load(file), formatter_file, sort_keys=True, indent=4, ensure_ascii=False)
