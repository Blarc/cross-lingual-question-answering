import json

f = open('train-v2.0_SL_fixed.json')

json_file = json.load(f)
new_data = {}

new_data['data'] = []

for data in json_file:
    for paragraph in data['paragraphs']:
        cur_context = paragraph['context']
        
        for question in paragraph['qas']:
            if len(question['answers']) > 0:
                new_ans_question = {}
                new_ans_question['context'] = cur_context
                new_ans_question['id'] = question['id']
                
                new_answer = {}
                new_answer['answer_start'] = []
                new_answer['text'] = []
                
                for answer in question['answers']:
                    #new_answer = {}
                    #new_answer['answer_start'] = []
                    new_answer['answer_start'].append(answer['answer_start'])
                    
                    #new_answer['text'] = []
                    new_answer['text'].append(answer['text'])
                    
                    new_ans_question['answers'] = new_answer
                    #break
                
                new_ans_question['question'] = question['question']
                new_ans_question['title'] = "something"
        
                new_data['data'].append(new_ans_question)
    

new_json = json.dumps(new_data)

with open("train.json", "w") as outfile:
    json.dump(new_data, outfile)

f.close()
