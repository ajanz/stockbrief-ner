import pandas as pd
from transformers import pipeline
from config.config import tagset, tagkey, tagother, regexes
import spacy
import re

class Inferator:
    def __init__(self) -> None:
        self.ner = pipeline('ner', model='clarin-pl/FastPDN', aggregation_strategy='max')
        self.nlp = spacy.load('pl_core_news_sm')

    def inferate(
        self,
        text: str,
        translated:bool = True,
    ) -> dict:
        # print([str(t) for t in self.nlp(text).sents])
        g = [self.ner(str(t)) for t in self.nlp(text).sents]
        if translated:
            return self.stockbrief_tagset_translate(g)
        return g

    def set_other(
        self,
        dct:dict,
    ):
        dct[tagkey] = tagother
        return dct


    def stockbrief_tagset_translate(
        self,
        sentence:list[dict],
    ):
        return [[x if x[tagkey] in tagset else self.set_other(x) for x in word] for word in sentence]


def proper_document(
    text:str,
    inferator:Inferator,
    rules:str,
) -> bool:
    for sentence in inferator.inferate(text):
        for entity in sentence:
            if entity['entity_group'] != tagother and re.match(rules, entity['word'], re.IGNORECASE):
                return True
    return False

def find_texts(
    path: str = "./data/"
    ) -> list:
    texts = list(pd.read_csv(path, header=None,sep=';')[0])
    combined_rules = "(" + ")|(".join(regexes) + ")"
    inferator = Inferator()

    return [text for text in texts if proper_document(text,inferator,combined_rules)]


if __name__ == '__main__':
    print(find_texts(path='./data/data.csv'))