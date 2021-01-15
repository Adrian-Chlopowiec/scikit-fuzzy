from skfuzzy.controlType2.antecedent_consequent import Antecedent, Consequent
from skfuzzy.controlType2.controlsystem import ControlSystem, ControlSystemSimulation
from skfuzzy.controlType2.rule import Rule
from skfuzzy.membership import sigmf

import pickle
import numpy as np
from tqdm import tqdm


def defineClassOne(x, center_point, width):
    y = np.zeros(len(x))
    idx = x <= center_point
    y[idx] = sigmf(x[idx], center_point, width)
    return y


def defineClassTwo(x, center_point, width):
    y = np.zeros(len(x))
    idx = x > center_point
    y[idx] = sigmf(x[idx], center_point, width)
    return y


def generate_rules(rule_antecedents, d_results, decision):
    rules = []
    for idx, x in enumerate(rule_antecedents):
        if x:
            rules.append(Rule(x, decision[d_results[idx]]))

    return rules


def makePrediction(row, classing, rules_feature_names, decision):
    input_values = {}
    for x in rules_feature_names:
        input_values[x] = row[x]

    classing.inputs(input_values)

    try:
        classing.compute()

    except:
        row['Predicted Value'] = 0.5
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return row

    row['Predicted Value'] = classing.output['Decision']
    return row


def main():
    tqdm.pandas()
    x_range = np.arange(0, 1, 0.001)
    d_results = ["Zero", "One"]
    rule_antecedents = pickle.load(open(r'Pickle\rule_antecedents.p', "rb"))
    decision = pickle.load(open(r'Pickle\decision.p', 'rb'))
    df = pickle.load(open(r'Pickle\dataframe.p', 'rb'))

    decision["One"] = defineClassOne(x_range, 0.5, 5)
    decision["Zero"] = defineClassTwo(x_range, 0.5, 5)

    rules = generate_rules(rule_antecedents, d_results, decision)
    class_ctrl = ControlSystem(rules)
    gen = class_ctrl.fuzzy_variables
    classing = ControlSystemSimulation(class_ctrl)
    rules_feature_names = []
    for x in gen:
        if str(x).startswith('Antecedent'):
            rules_feature_names.append(str(x).split(': ')[1])

    df = df.progress_apply(makePrediction, classing=classing, rules_feature_names=rules_feature_names,
                           decision=decision, axis=1)
    print("Done")


if __name__ == '__main__':
    main()
