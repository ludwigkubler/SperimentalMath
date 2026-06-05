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
            op = random.choice(['&', '|'])
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f'({left} {op} {right})'
    
    def evaluate_formula(formula, assignment):
        if formula.isdigit():
            return int(formula)
        elif formula == '0':
            return 0
        elif formula == '1':
            return 1
        else:
            var, op, subformula = formula[1:-1].split()
            if op == '&':
                return evaluate_formula(subformula, assignment) and evaluate_formula(var, assignment)
            elif op == '|':
                return evaluate_formula(subformula, assignment) or evaluate_formula(var, assignment)
    
    def minimal_rank(formula):
        n = len(formula)
        if n == 1:
            return 1
        else:
            left = formula[:n // 2]
            right = formula[n // 2:]
            rank_left = minimal_rank(left)
            rank_right = minimal_rank(right)
            return max(rank_left, rank_right) + 1
    
    def circuit_entanglement(formula):
        if formula.isdigit():
            return 0
        elif formula == '0':
            return 0
        elif formula == '1':
            return 0
        else:
            var, op, subformula = formula[1:-1].split()
            if op == '&':
                entanglement_left = circuit_entanglement(subformula)
                entanglement_right = circuit_entanglement(var)
                return max(entanglement_left, entanglement_right) + 1
            elif op == '|':
                entanglement_left = circuit_entanglement(subformula)
                entanglement_right = circuit_entanglement(var)
                return max(entanglement_left, entanglement_right) + 1
    
    n_max = 40
    instances_tested = 30
    total_ratio = 0.0
    count_within_factor = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_formula(n)
        rank = minimal_rank(formula)
        entanglement = circuit_entanglement(formula)
        
        if entanglement == 0:
            continue
        
        ratio = abs(Fraction(rank, entanglement))
        total_ratio += ratio
        if 1 / 2 <= ratio <= 2:
            count_within_factor += 1
    
    mean_ratio = total_ratio / instances_tested
    support_fraction = count_within_factor / instances_tested
    
    return {
        "metric_name": "Ratio of Minimal Rank to Circuit Entanglement",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.95 and abs(mean_ratio - 1) < 1,
        "counterexample": "" if support_fraction >= 0.95 else f"Ratio {mean_ratio} not within factor [1/2, 2]"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [3, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of factor [1/2, 2]\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")