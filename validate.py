
from inferate import Inferator
from config.config import regexes, tagkey, tagother
import ast
import re

def get_regular_form(
    text:str,
) ->str:
    text = text.lower()
    combined_rules = "(" + ")|(".join(regexes) + ")".lower()
    g = re.match(combined_rules, text, re.IGNORECASE) # doens't find pko in ipko...

    if g is None:
        return ''
    return g.group()




def get_entities_stats(
    list_of_entities:list[dict],
)->dict:
    res = {}
    for entity in list_of_entities:
        if entity[tagkey] == tagother:
            continue
        rf = get_regular_form(entity['word'])
        if rf == '':
            continue
        if (rf, entity[tagkey]) not in res:
            res[(rf, entity[tagkey])] = 1
            continue
        res[(rf, entity[tagkey])] += 1
    return res

def validate():
    with open("./data/test/test_data.txt", "r") as f:
        text = f.read()
    inferator = Inferator()
    results = inferator.inferate(text = text)
    
    with open("./data/test/test_y.txt", "r") as f:
        text_y = f.read()
    reals = ast.literal_eval(text_y)

    all_,proper = 0,0
    # print(results)
    for pred, real in zip(results,reals):
        if real == pred:
            proper+=1
            all_+=1
            continue
        # print(pred)
        pred_counted = get_entities_stats(pred)
        real_counted = get_entities_stats(real)

        for k in pred_counted.keys() & real_counted.keys():
            proper+=min([pred_counted[k],real_counted[k]])
            all_+=max([pred_counted[k],real_counted[k]])

        for k in set(pred_counted.keys()).difference(real_counted.keys()):
            print(pred_counted[k])
            all_ += pred_counted[k]

        for k in set(real_counted.keys()).difference(pred_counted.keys()):
            print(real_counted[k])
            all_ += real_counted[k]
            print('###############')
        

    print(proper/all_)


        
#         print(f"""XXXXXXXXXXXXX
# real: {real}
# pred: {pred}""")

    

if __name__ == '__main__':
    validate()