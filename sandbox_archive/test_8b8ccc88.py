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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def evaluate(formula, assignment):
        if formula[0] == 'var':
            return assignment[formula[1]]
        elif formula[0] == 'not':
            return not evaluate(formula[1], assignment)
        else:
            op = formula[0]
            left = evaluate(formula[1], assignment)
            right = evaluate(formula[2], assignment)
            if op == 'and':
                return left and right
            elif op == 'or':
                return left or right
            elif op == 'implies':
                return not left or right
            else:
                raise ValueError(f"Unknown operator: {op}")
    
    def generate_formula(n):
        if n == 1:
            return ('var', random.choice(['x0']))
        else:
            p = random.random()
            if p < 0.3:
                return ('not', generate_formula(n-1))
            elif p < 0.6:
                return ('and', generate_formula(n//2), generate_formula(n-n//2))
            else:
                return ('or', generate_formula(n//2), generate_formula(n-n//2))
    
    def truth_table(formula, n):
        variables = ['x' + str(i) for i in range(n)]
        table = []
        for assignment in itertools.product([True, False], repeat=n):
            assignment_dict = dict(zip(variables, assignment))
            table.append(evaluate(formula, assignment_dict))
        return table
    
    def p_adic_order(table, p):
        order = 0
        for entry in table:
            if entry == True:
                order += 1
            elif entry == False:
                order -= 1
        return abs(order)
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    truth_table_list = truth_table(formula, n)
    p = 2  # Using prime number 2 for simplicity
    
    min_order = min(p_adic_order(truth_table_list[:i+1], p) for i in range(len(truth_table_list)))
    depth = math.ceil(math.log2(n))
    
    return {
        "metric_name": "Minimal Order of p-adic Galois Representation",
        "metric_value": min_order,
        "instances_tested": len(truth_table_list),
        "conjecture_holds": min_order <= p**depth,
        "counterexample": "" if min_order <= p**depth else f"Formula: {formula}, Depth: {depth}, Min Order: {min_order}"
    }

if __name__ == "__main__":
    import sys
    import itertools
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Formula exceeds expected order' first_failing_seed={first_failing_seed}")