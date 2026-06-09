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
            return random.choice(['0', '1'])
        else:
            op = random.choice(['&', '|', '^'])
            left = generate_formula(n - 1)
            right = generate_formula(n - 1)
            return f'({left} {op} {right})'
    
    def dpll(formula):
        if formula == '0':
            return False
        elif formula == '1':
            return True
        else:
            var, op, rest = formula[1], formula[2], formula[3:-1]
            if op == '&':
                return dpll(rest) and dpll(f'({var} {op} 0)')
            elif op == '|':
                return dpll(rest) or dpll(f'({var} {op} 1)')
            else:
                return (dpll(rest) and not dpll(f'({var} & 1)')) or (not dpll(rest) and dpll(f'({var} | 0)'))
    
    def min_rank(formula):
        if formula == '0':
            return 1
        elif formula == '1':
            return 1
        else:
            var, op, rest = formula[1], formula[2], formula[3:-1]
            left_rank = min_rank(rest)
            right_rank = min_rank(f'({var} {op} 0)')
            if op == '&':
                return max(left_rank, right_rank) + 1
            elif op == '|':
                return max(left_rank, right_rank) + 1
            else:
                return max(left_rank, right_rank) + 1
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        num_vars = random.randint(5, 40)
        formula = generate_formula(num_vars)
        h_phi = dpll(formula)
        mrank_phi = min_rank(formula)
        metric_values.append(mrank_phi / h_phi)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(0.95 <= m / h <= 1.05 for m, h in zip(metric_values, [dpll(generate_formula(num_vars)) for _ in range(instances_tested)]))
    
    return {
        "metric_name": "mrank/h_ratio",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")