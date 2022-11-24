
from inferate import Inferator
from config.config import regexes, tagkey, tagother
import ast
import re


def get_regular_form(
    text:str,
) ->str:
    text = text.lower()
    combined_rules = "(" + ")|(".join(regexes) + ")".lower()
    found_texts = re.findall(combined_rules,text, re.IGNORECASE)
    if len(found_texts) == 0:
        return ''
    return found_texts[0]

def get_entities_stats(
    list_of_entities:list[dict],
    regular_form:bool = True,
)->dict:
    res = {}
    for entity in list_of_entities:
        if entity[tagkey] == tagother and regular_form:
            continue
        rf = entity['word']
        if regular_form:
            rf = get_regular_form(entity['word'])
        if rf == '':
            continue
        if (rf, entity[tagkey]) not in res:
            res[(rf, entity[tagkey])] = 1
            continue
        resv = res[(rf, entity[tagkey])] 
        resv+=1
        res[(rf, entity[tagkey])] = resv
    return res


def get_duplicates(
    s1:set,
    s2:set,
)->int:
    duplicates = 0
    for v1 in s1:
        for v2 in s2:
            if v2[0] == v1[0]:
                duplicates+=1
                continue
            if v2[1] == v1[1] and (v1[0][:6] == v2[0][:6] or v1[0][-6:] == v2[0][-6:]):
                duplicates+=1
                continue
    return duplicates


def validate_set(
    data_path: str,
    y_path: str,
    regular_form: bool,
    ) -> float:
    with open(data_path, "r") as f:
        text = f.read()
    inferator = Inferator()
    results = inferator.inferate(text = text)
    
    with open(y_path, "r") as f:
        text_y = f.read()
    reals = ast.literal_eval(text_y)
    all_,proper = 0,0
    for pred, real in zip(results,reals):
        if real == pred:
            proper+=1
            all_+=1
            continue
        pred_counted = get_entities_stats(pred, regular_form)
        real_counted = get_entities_stats(real, regular_form)

        for k in pred_counted.keys() & real_counted.keys():
            proper+=min([pred_counted[k],real_counted[k]])
            all_+=max([pred_counted[k],real_counted[k]])

        pred_diff = set(pred_counted.keys()).difference(real_counted.keys())
        for k in pred_diff:
            all_ += pred_counted[k]

        real_diff = set(real_counted.keys()).difference(pred_counted.keys())
        for k in real_diff:
            all_ += real_counted[k]
        all_ = all_ - get_duplicates(pred_diff,real_diff)

    return proper/all_

if __name__ == '__main__':
    acc_1 = validate_set(
        data_path="./data/test/test_data.txt",
        y_path="./data/test/test_y2.txt",
        regular_form=False,
    )
    acc_2 = validate_set(
        data_path="./data/test/test_data.txt",
        y_path="./data/test/test_y.txt",
        regular_form=True,
    )
    print(f"""
Acc all labels: {acc_1}
Acc regexed labels: {acc_2}""")