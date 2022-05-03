import os

from translation_utils import clean_text


def clean_lines(data):
    """
    Cleans lines of split data.
    
    :param data: Train or dev dataset.
    :return: Cleaned lines in specified directory.
    """
    for filename in os.listdir(f'../../data/tmp/{data}'):
        file_path = os.path.join(f'../../data/tmp/{data}', filename)
        
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as in_file:
                with open(f'../../data/tmp/{data}_clean/{filename[:-4]}_clean.txt', 'w', encoding='utf-8') as out_file:
                    for line in in_file.readlines():
                        print(clean_text(line).lstrip().rstrip(), file=out_file)


if __name__ == '__main__':
    clean_lines('dev')
    