import json
import fasttext

from src.utils.translation_utils import find_similar_text, clean_text


def fix_translated_answers(data_name, model):
    print('Loading model...')
    model = fasttext.load_model(model)
    print('Model loaded!')

    with open(f'../data/{data_name}-v2.0_SL.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)

    for theme_index, theme in enumerate(data):
        print(f'{theme_index} / {len(data)}')
        for paragraph in theme['paragraphs']:
            context = paragraph['context']
            context = clean_text(context)
            for qas in paragraph['qas']:
                question = qas['question']
                for answer in qas['answers']:
                    answer_text = answer['text']
                    answer_text = clean_text(answer_text).rstrip()
                    answer_start = int(answer['answer_start'])
                    answer_split = answer_text.split(' ')
                    
                    # print('-' * 100)
                    # print(f'search_context: {context[max(answer_start - 200, 0): min(answer_start + len(answer_text) + 200, len(context))]}')
                    # print(f'question: {question}')
                    # print(f'before: {answer_text}')
                    
                    reduced_context = context[max(answer_start - 200, 0): min(answer_start + len(answer_text) + 200, len(context))].lstrip()
                    reduced_context_split = reduced_context.split(' ')
                    start_index, end_index, similarity, avg_similarities, best_grams = find_similar_text(answer_text, reduced_context, model, 1)
                    
                    if start_index > end_index:
                        tmp = start_index
                        start_index = end_index
                        end_index = tmp

                    # print(f'after: {" ".join(reduced_context_split[start_index:start_index + len(answer_split)])}')
                    # print(f'indexes: {start_index} : {end_index}')
                    # print(f'similarity: {similarity}')
                    # print(f'avg similarties: {avg_similarities}')
                    # print(f'best grams: {best_grams}')
                    
                    if similarity > 0.985:
                        answer['text'] = " ".join(reduced_context_split[start_index:start_index + len(answer_split)])

                if 'plausible_answers' in qas:
                    for plausible_answer in qas['plausible_answers']:
                        plausible_answer = plausible_answer['text']
        
    with open(f'../data/{data_name}-v2.0_SL-fixed.json', 'w', encoding='UTF-8') as file:
        json.dump(json.load(file), file, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    model_name = 'train'
    fix_translated_answers('dev', f'../models/cc.sl.300.bin')
