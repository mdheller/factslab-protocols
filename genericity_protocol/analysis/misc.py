# data = data.rename(columns={'worker_id':'Annotator.ID', 'sent_id':'Sentence.ID',
#                               'pred_root_token':'Pred.Root.Token', 'pred_token':'Pred.Tokens',
#                               'predicate':'Predicate', 'lemma':'Predicate.Lemma',
#                               'part':'Is.Particular', 'part_conf':'Part.Confidence',
#                               'dyn':'Is.Dynamic', 'dyn_conf':'Dyn.Confidence',
#                               'hyp':'Is.Hypothetical', 'hyp_conf':'Hyp.Confidence'})
# data.to_csv('pred_raw_data.tsv', sep="\t", index=False)

# hits = pd.read_csv('pred_hits_rerun.tsv', sep="\t")
# raw_dat_file = raw_data_file.append(raw_data_file_c, ignore_index=True)
# raw_dat_file = raw_dat_file[raw_dat_file.AssignmentStatus != "Rejected"]

# hits_to_rerun = raw_dat_file[raw_dat_file.WorkerId.isin(hits.annotator.values.tolist())]
# with open('pred_rerun.csv', 'w') as f:
#     f.write("var_arrays\n")
#     for out_data in hits_to_rerun["Input_var_arrays"].values.tolist():
#         f.write("\"" + replace_string(str(out_data)) + "\"\n")

# print(hits.hits.values.tolist().sort() == hits_to_rerun.HITId.values.tolist().sort())

# from collections import Counter
# from collections import defaultdict
# rev = defaultdict(list)
# datum['sent_pred'] = datum['Sentence.ID'].map(lambda x : x) + "_" + datum['Pred.Tokens'].map(lambda x: str(x))
# mbc = Counter(datum['sent_pred'].values.tolist())
# for k, v in mbc.items():
#     rev[v].append(k)
# # print(rev.keys())
# print(len(rev[3]))
# print(len(rev[2]))
# print(len(rev[6]))
# # print(datum[datum['Sentence.ID'] == 'en-ud-test.conllu sent_1233'])
# # print(mbc)
# # datum['Split']

# from statistics import mode

# attributes = ["part", "kind", "abs"]
# attr_map = {"part": "Is.Particular", "kind": "Is.Kind", "abs": "Is.Abstract"}
# attr_conf = {"part": "Part.Confidence", "kind": "Kind.Confidence",
#              "abs": "Abs.Confidence"}
# response = ["Is.Particular", "Is.Kind", "Is.Abstract"]
# response_conf = ["Part.Confidence", "Kind.Confidence", "Abs.Confidence"]

# data_dev = long_data[long_data['Split'] != 'test']
# data_dev = data_dev[data_dev['Split'] != 'train']

# # Convert responses to 1s and 0s
# for resp in response:
#     data_dev[resp] = data[resp].astype(int)

# for resp in response_conf:
#     data_dev[resp] = data.groupby('Annotator.ID')[resp].apply(lambda x: x.rank() / (len(x) + 1.))
# data_dev = data[data['Split'] == 'dev']
# col = data_dev['Sentence.ID'] + "_" + data_dev['Noun.Token'].map(str)
# data_dev = data_dev.assign(SentenceIDToken=col.values)
# sent_ids = list(set(data_dev['SentenceIDToken'].tolist()))
# data_dev_reduced = pd.DataFrame()
# i = 0
# for sent_id in sent_ids:
#     i += 1
#     new_df = data_dev[data_dev['SentenceIDToken'] == sent_id]
#     sample = new_df.iloc[0]
#     for attr in attributes:
#         answers = new_df[attr_map[attr]].tolist()
#         if all(x == answers[0] for x in answers):
#             mode_ans = answers[0]
#             new_conf = sum(new_df[attr_conf[attr]].tolist()) / 3
#         else:
#             print(sent_id, end="\r")
#             mode_ans = mode(answers)
#             new_df[new_df[attr_map[attr]] != mode_ans][attr_conf[attr]] = 1 - new_df[new_df[attr_map[attr]] != mode_ans][attr_conf[attr]]
#             new_conf = sum(new_df[attr_conf[attr]].tolist()) / 3

#         sample[attr_map[attr]] = mode_ans
#         sample[attr_conf[attr]] = new_conf

#     data_dev_reduced = data_dev_reduced.append(sample)
# data_dev_reduced.to_csv('../../../data/noun_data_dev.tsv', sep='\t', index=False)

# data = data.rename(columns={'worker_id':'Annotator.ID', 'sent_id':'Sentence.ID',
#                                       'noun_token':'Noun.Token', 'lemma': 'Noun.Lemma',
#                                       'noun':'Noun', 'part':'Is.Particular', 
#                                       'part_conf':'Part.Confidence', 'kind':'Is.Kind', 
#                                       'kind_conf':'Kind.Confidence', 'abs':'Is.Abstract', 
#                                       'abs_conf':'Abs.Confidence'})
# data.to_csv('noun_raw_data.tsv', sep="\t", index=False)

# hits = pd.read_csv('noun_hits_rerun.tsv', sep="\t")
# raw_data_file = raw_data_file[raw_data_file.AssignmentStatus != "Rejected"]

# hits_to_rerun = raw_data_file[raw_data_file.WorkerId.isin(hits.annotator.values.tolist())]
# with open('noun_rerun.csv', 'w') as f:
#     f.write("var_arrays\n")
#     for out_data in hits_to_rerun["Input_var_arrays"].values.tolist():
#         f.write("\"" + replace_string(str(out_data)) + "\"\n")

# print(hits.hits.values.tolist().sort() == hits_to_rerun.HITId.values.tolist().sort())
