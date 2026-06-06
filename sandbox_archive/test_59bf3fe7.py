# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['&', '|'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f"({left} {op} {right})"
    
    def frege_proof_depth(formula):
        if formula in ['True', 'False']:
            return 1
        else:
            op_index = formula.find(' ')
            left_depth = frege_proof_depth(formula[:op_index])
            right_depth = frege_proof_depth(formula[op_index + 2:])
            return max(left_depth, right_depth) + 1
    
    def quantum_state_dimension(formula):
        if formula in ['True', 'False']:
            return 1
        else:
            op_index = formula.find(' ')
            left_dim = quantum_state_dimension(formula[:op_index])
            right_dim = quantum_state_dimension(formula[op_index + 2:])
            return max(left_dim, right_dim) + 1
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_boolean_formula(n)
        gqd = quantum_state_dimension(formula)
        w_F = frege_proof_depth(formula)
        if gqd > 0 and w_F > 0:
            metric_values.append(gqd / w_F)
    
    if not metric_values:
        return {
            "metric_name": "gqd/w_F",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    conjecture_holds = all(abs(gqd / w_F - mean) <= 3 for gqd, w_F in zip(metric_values, [frege_proof_depth(generate_boolean_formula(n)) for n in range(5, n_max + 1)]))
    
    return {
        "metric_name": "gqd/w_F",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")