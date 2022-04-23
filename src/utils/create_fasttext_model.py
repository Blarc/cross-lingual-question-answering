import json
import fasttext


def create_fasttext_model(data_name):
    """
    Creates a fasttext model for word embeddings only on the contexts
    and saves it to file.
    
    :param data_name: name of the data file (train, dev)
    """
    with open(f'../../data/{data_name}-v2.0_SL.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)

    with open(f'../../data/tmp/{data_name}-contexts-merged.txt', 'w', encoding='UTF-8') as file:
        for theme in data:
            for paragraph in theme['paragraphs']:
                print(paragraph['context'], file=file)
    
    # TODO: Pre-proccess text before training the model.
    # TODO: Test different parameters (i.e. wordNgrams)
    model = fasttext.train_unsupervised(f'../../data/tmp/{data_name}-contexts-merged.txt', wordNgrams=3)
    model.save_model(f'../../models/fasttext_{data_name}_model.bin')


if __name__ == '__main__':
    create_fasttext_model('train')
