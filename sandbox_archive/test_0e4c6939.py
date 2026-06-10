# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['and', 'or'])
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            return f"({subformulas[0]} {op} {subformulas[1]})"
    
    def dpll(formula):
        if formula == 'True':
            return 1
        elif formula == 'False':
            return 0
        else:
            subformulas = formula.split(' ')[2].split(',')
            return max(dpll(subformulas[0]), dpll(subformulas[1])) + 1
    
    def tseitin(formula):
        if formula == 'True' or formula == 'False':
            return formula
        elif 'and' in formula:
            subformulas = formula.split(' ')[2].split(',')
            x, y = random.randint(0, 100), random.randint(0, 100)
            tseitin_x = f"t{x}"
            tseitin_y = f"t{y}"
            return f"{tseitin_x} and {tseitin_y}"
        elif 'or' in formula:
            subformulas = formula.split(' ')[2].split(',')
            x, y = random.randint(0, 100), random.randint(0, 100)
            tseitin_x = f"t{x}"
            tseitin_y = f"t{y}"
            return f"{tseitin_x} or {tseitin_y}"
    
    def tropical_hodge_index(formula):
        if formula == 'True' or formula == 'False':
            return 0
        elif 'and' in formula:
            subformulas = formula.split(' ')[2].split(',')
            return max(tropical_hodge_index(subformulas[0]), tropical_hodge_index(subformulas[1]))
        elif 'or' in formula:
            subformulas = formula.split(' ')[2].split(',')
            return max(tropical_hodge_index(subformulas[0]), tropical_hodge_index(subformulas[1]))
    
    n_values = [5, 10, 15, 20, 30, 40]
    thi_sum = 0
    d_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_formula(n)
            thi_value = tropical_hodge_index(formula)
            d_value = dpll(formula)
            thi_sum += thi_value
            d_sum += d_value
            instances_tested += 1
    
    mean_thi = Fraction(thi_sum, instances_tested)
    mean_d = Fraction(d_sum, instances_tested)
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    pearson_corr = (instances_tested * thi_sum * d_sum - thi_sum * thi_sum - d_sum * d_sum) / \
                   math.sqrt((instances_tested * thi_sum * thi_sum - thi_sum * thi_sum) *
                             (instances_tested * d_sum * d_sum - d_sum * d_sum))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r['conjecture_holds'] for r in results):
        mean_value = sum(r['metric_value'] for r in results) / len(results)
        std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r['conjecture_holds']]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r['counterexample'] == "not_enough_instances" for r in results):
        print("RESULT: INCONCLUSIVE not_enough_instances")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_data\" first_failing_seed={first_failing_seed}")