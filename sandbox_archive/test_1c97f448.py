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
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            op = random.choice(['&', '|', '^'])
            return f'({subformulas[0]} {op} {subformulas[1]})'
    
    def evaluate_formula(formula):
        if formula == '0':
            return 0
        elif formula == '1':
            return 1
        else:
            left, op, right = formula.split()
            left_val = evaluate_formula(left)
            right_val = evaluate_formula(right)
            if op == '&':
                return left_val & right_val
            elif op == '|':
                return left_val | right_val
            elif op == '^':
                return left_val ^ right_val
    
    def minimal_rank(formula):
        n = len(formula)
        rank = 0
        for i in range(1 << n):
            assignment = [bool(i & (1 << j)) for j in range(n)]
            if evaluate_formula(formula, assignment) == 1:
                rank += 1
        return rank
    
    def circuit_entanglement(formula):
        # Simplified entanglement measure based on formula structure
        n = len(formula)
        return n * (n - 1) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_formula(n)
            rank = minimal_rank(formula)
            entanglement = circuit_entanglement(formula)
            if entanglement == 0:
                continue
            ratio = abs(rank / entanglement)
            results.append((n, rank, entanglement, ratio))
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _, _, _ in results)
    mean_ratio = sum(ratio for _, _, _, ratio in results) / len(results)
    std_ratio = math.sqrt(sum((ratio - mean_ratio) ** 2 for _, _, _, ratio in results) / len(results))
    support_fraction = sum(1 for _, _, _, ratio in results if abs(ratio - 1) < 0.5) / len(results)
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.95 and std_ratio < 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(abs(r["metric_value"] - 1) >= 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")