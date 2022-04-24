import json
import fasttext

from translation_utils import clean_text


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
                context = paragraph['context']
                context = clean_text(context)
                print(context, file=file)

    # TODO: Pre-proccess text before training the model.
    # TODO: Test different parameters (i.e. wordNgrams)
    model = fasttext.train_unsupervised(f'../../data/tmp/{data_name}-contexts-merged.txt', wordNgrams=1)
    model.save_model(f'../../models/fasttext_{data_name}_model.bin')


if __name__ == '__main__':
    print('DEPRECATED: Use pretrained FastText model cc.sl.300.bin that can be downloaded from FastText website.')
    create_fasttext_model('dev')
