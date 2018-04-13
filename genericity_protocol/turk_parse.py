from predpatt import load_conllu
from predpatt import PredPatt
from json import dumps
import random
import os

id = 1
out_data = []
files = ['/UD_English-r1.2/en-ud-train.conllu', '/UD_English-r1.2/en-ud-test.conllu', '/UD_English-r1.2/en-ud-dev.conllu']
with open('dataset.csv', 'w') as outfile:
    outfile.write("var_arrays\n")
    for file in files:
        path = os.getcwd() + file
        with open(path, 'r') as infile:
            data = infile.read()
            parsed = [PredPatt(ud_parse) for sent_id, ud_parse in load_conllu(data)]
            # random.shuffle(parsed)
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
                        pred_sentence.insert(pred_token, "<span class=\\\'\'predicate\'\'\\>")
                        pred_sentence.insert(pred_token + 2, '</span>')
                        noun_sentence.insert(noun_token, "<span class=\\\'\'noun\'\'\\>")
                        noun_sentence.insert(noun_token + 2 + len(noun.split()), '</span>')
                        # token_dict['"{}"'.format('raw_sentence')] = '"{}"'.format(" " + " ".join(raw_sentence) + " ")
                        # token_dict['"{}"'.format('id')] = id
                        # token_dict['"{}"'.format('pred')] = '"{}"'.format(pred)
                        # token_dict['"{}"'.format('pred_token')] = '"{}"'.format(pred_token)
                        # token_dict['"{}"'.format('noun')] = '"{}"'.format(noun)
                        # token_dict['"{}"'.format('noun_token')] = '"{}"'.format(noun_token)
                        # token_dict['"{}"'.format('pred_sentence')] = '"{}"'.format(" " + " ".join(pred_sentence) + " ")
                        # token_dict['"{}"'.format('noun_sentence')] = '"{}"'.format(" " + " ".join(noun_sentence) + " ")
                        token_dict['raw_sentence'] = "'{}'".format(" " + " ".join(raw_sentence) + " ")
                        token_dict['id'] = id
                        token_dict['pred'] = "'{}'".format(pred)
                        token_dict['pred_token'] = "'{}'".format(pred_token)
                        token_dict['noun'] = "'{}'".format(noun)
                        token_dict['noun_token'] = "'{}'".format(noun_token)
                        token_dict['pred_sentence'] = "'{}'".format(" " + " ".join(pred_sentence) + " ")
                        token_dict['noun_sentence'] = "'{}'".format(" " + " ".join(noun_sentence) + " ")
                        out_data.append(dumps(token_dict))
                        id += 1
                        if id == 11:
                            id = 0
                            outfile.write("\"" + str(out_data) + "\"\n")
                            out_data = []
