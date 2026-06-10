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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(random.randint(2, n))]
            operator = random.choice(['&', '|'])
            return f'({subformulas[0]} {operator} {subformulas[1]})'
    
    def incidence_poset(formula):
        if formula.isdigit():
            return set([formula])
        elif formula.startswith('(') and formula.endswith(')'):
            left, operator, right = formula[1:-1].split()
            poset_left = incidence_poset(left)
            poset_right = incidence_poset(right)
            return poset_left.union(poset_right).union({f'({x} {operator} {y})' for x in poset_left for y in poset_right})
        else:
            raise ValueError("Invalid formula")
    
    def ehrhart_semigroup_size(poset):
        if not poset:
            return 0
        n = len(poset)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            M[i][i-1] = 1
            M[0][i] = 1
        for i in range(2, n + 1):
            for j in range(i - 2, -1, -1):
                M[j][i] = sum(M[k][j] for k in range(j + 1, i))
        return M[0][-1]
    
    def resolution_proof_width(formula):
        if formula.isdigit():
            return 1
        elif formula.startswith('(') and formula.endswith(')'):
            left, operator, right = formula[1:-1].split()
            width_left = resolution_proof_width(left)
            width_right = resolution_proof_width(right)
            return max(width_left, width_right) + 1
        else:
            raise ValueError("Invalid formula")
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_boolean_formula(n)
        poset = incidence_poset(formula)
        ehrhart_size = ehrhart_semigroup_size(poset)
        width = resolution_proof_width(formula)
        
        metric_values.append(ehrhart_size - width)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    correlation_coefficient = sum(x * y for x, y in zip(metric_values, range(5, n_max + 1))) / (len(metric_values) * n_max)
    
    if correlation_coefficient < 0.8 or abs(mean_value) > 3:
        conjecture_holds = False
        counterexample = "correlation_coefficient<0.8 or mean_value>3"
    
    return {
        "metric_name": "Ehrhart_semigroup_size - Resolution_proof_width",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")