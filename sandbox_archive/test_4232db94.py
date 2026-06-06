# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations, permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def quantum_state_dimension(formula):
        if formula == '0' or formula == '1':
            return 1
        elif formula.startswith('¬'):
            return quantum_state_dimension(formula[1:])
        else:
            op_index = next(i for i, char in enumerate(formula) if char in ('∧', '∨'))
            left_dim = quantum_state_dimension(formula[:op_index])
            right_dim = quantum_state_dimension(formula[op_index + 1:])
            return left_dim * right_dim
    
    def frege_proof_depth(formula):
        if formula == '0' or formula == '1':
            return 1
        elif formula.startswith('¬'):
            return 1 + frege_proof_depth(formula[1:])
        else:
            op_index = next(i for i, char in enumerate(formula) if char in ('∧', '∨'))
            left_depth = frege_proof_depth(formula[:op_index])
            right_depth = frege_proof_depth(formula[op_index + 1:])
            return 1 + max(left_depth, right_depth)
    
    def generate_random_formula(n):
        if n == 0:
            return random.choice(['0', '1'])
        else:
            variables = list(range(1, n + 1))
            formula = []
            for _ in range(random.randint(1, n)):
                op = random.choice(['∧', '∨'])
                args = [generate_random_formula(n - 1) for _ in range(2)]
                formula.append(f'({op.join(args)})')
            return '(' + ' '.join(formula) + ')'
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_random_formula(n)
            gqd = quantum_state_dimension(formula)
            w_F = frege_proof_depth(formula)
            results.append((gqd, w_F))
    
    if not results:
        return {
            "metric_name": "GQD / w_F",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No formulas generated"
        }
    
    gqd_values = [gqd for gqd, _ in results]
    w_F_values = [w_F for _, w_F in results]
    mean_gqd = sum(gqd_values) / len(gqd_values)
    mean_w_F = sum(w_F_values) / len(w_F_values)
    ratio = mean_gqd / mean_w_F
    diff = abs(mean_gqd - mean_w_F)
    
    return {
        "metric_name": "GQD / w_F",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(n for _, n in [(gqd, n) for gqd, _ in results]),
        "conjecture_holds": ratio > 1.0 and diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_dev = (sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))**0.5
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")