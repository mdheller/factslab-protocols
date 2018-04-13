from predpatt import load_conllu
from predpatt import PredPatt
import random
import os

id = 1
out_data = []
file = '/UD_English-r1.2/en-ud-train.conllu'
path = os.getcwd() + file
with open(path, 'r') as infile:
    data = infile.read()
    parsed = [PredPatt(ud_parse) for sent_id, ud_parse in load_conllu(data)]
    # random.shuffle(parsed)
    with open('dataset.csv', 'w') as outfile:
        outfile.write("var_arrays\n")
        for parse_sen in parsed:
            for predicate in parse_sen.instances:
                raw_sentence = [token.text for token in parse_sen.tokens]
                pred_token = predicate.root.position
                pred = predicate.root.text
                for argument in predicate.arguments:
                    token_dict = {}
                    noun = " ".join(token.text for token in argument.tokens)
                    noun_token = raw_sentence.index(noun.split()[0])
                    pred_sentence = raw_sentence.copy()
                    noun_sentence = raw_sentence.copy()
                    pred_sentence.insert(pred_token, '<span class="predicate">')
                    pred_sentence.insert(pred_token + 2, '</span>')
                    noun_sentence.insert(noun_token, '<span class="noun">')
                    noun_sentence.insert(noun_token + 2 + len(noun.split()), '</span>')
                    token_dict['raw_sentence'] = " ".join(raw_sentence)
                    token_dict['id'] = id
                    token_dict['pred'] = pred
                    token_dict['pred_token'] = pred_token
                    token_dict['noun'] = noun
                    token_dict['noun_token'] = noun_token
                    token_dict['pred_sentence'] = " ".join(pred_sentence)
                    token_dict['noun_sentence'] = " ".join(noun_sentence)
                    out_data.append(token_dict)
                    id += 1
                    if id == 11:
                        id = 0
                        outfile.write(str(str(out_data)) + "\n")
                        out_data = []
