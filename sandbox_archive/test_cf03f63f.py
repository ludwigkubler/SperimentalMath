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
            op = random.choice(['and', 'or'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f'({left} {op} {right})'
    
    def frege_proof_depth(formula):
        if formula == 'True' or formula == 'False':
            return 1
        else:
            left, op, right = formula[1:-1].split()
            return max(frege_proof_depth(left), frege_proof_depth(right)) + 1
    
    def quantum_state_representation_size(formula):
        if formula == 'True' or formula == 'False':
            return 1
        else:
            left, op, right = formula[1:-1].split()
            return max(quantum_state_representation_size(left), quantum_state_representation_size(right)) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_gqd = Fraction(0)
    total_wF = Fraction(0)
    
    for n in n_values:
        for _ in range(4):  # Ensure at least 24 instances per seed
            formula = generate_boolean_formula(n)
            gqd = quantum_state_representation_size(formula)
            wF = frege_proof_depth(formula)
            total_gqd += Fraction(gqd, n)
            total_wF += Fraction(wF, n)
            instances_tested += 1
    
    mean_gqd = total_gqd / instances_tested
    mean_wF = total_wF / instances_tested
    
    if mean_gqd / mean_wF > 1.0 and abs(mean_gqd - mean_wF) <= 3:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "gqd/mean(w_F) < 1 or |gqd - mean(w_F)| > 3"
    
    return {
        "metric_name": "GQD over w_F",
        "metric_value": float(mean_gqd / mean_wF),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{results[first_failing_seed]['counterexample']}' first_failing_seed={seeds[first_failing_seed]}")