import json
import jsonlines
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances


class BasicExampleSelector(object):
    def __init__(self):

        ##得到所有的问题和sql语句
        with open('few_shot/QA.json', 'r') as jsonl_f:
            dev_json = json.load(jsonl_f)
            self.train_json = dev_json
            self.train_questions = [obj['question'] for obj in dev_json]
            self.sql_jsonl = [obj['sql'] for obj in dev_json]


class EuclideanDistanceQuestionMaskSelector(BasicExampleSelector):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.SELECT_MODEL = "few_shot/sentence_transformers"
        self.mask_token = "<mask>"  # the "<mask>" is the mask token of all-mpnet-base-v2
        self.value_token = "<unk>"  # the "<unk>" is the unknown token of all-mpnet-base-v2

        ### 得到所有的问题
        train_mask_questions = self.train_questions
        self.bert_model = SentenceTransformer(self.SELECT_MODEL, device="cpu")
        self.train_embeddings = self.bert_model.encode(train_mask_questions, show_progress_bar=False)

    def get_examples(self, target, num_example):

        target_mask_question = target['question']
        target_embedding = self.bert_model.encode(target_mask_question, show_progress_bar=False).reshape(1, -1)


        # find the most similar question in train dataset
        distances = np.squeeze(euclidean_distances(target_embedding, self.train_embeddings)).tolist()
        pairs = [(distance, index) for distance, index in zip(distances, range(len(distances)))]

        train_json = self.train_json
        pairs_sorted = sorted(pairs, key=lambda x: x[0])
        top_pairs = list()
        for d, index in pairs_sorted:
            top_pairs.append((index, d))
            if len(top_pairs) >= num_example:
                break

        return [train_json[index] for (index, d) in top_pairs]
