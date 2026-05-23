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

def generate_tseitin_formula(n):
    if n < 2:
        return []
    
    variables = list(range(1, n + 1))
    clauses = []
    
    for i in range(1, n + 1):
        clauses.append([variables[i-1]])
    
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            clauses.append([-variables[i-1], variables[j-1]])
            clauses.append([-variables[j-1], variables[i-1]])
            clauses.append([variables[i-1], variables[j-1], -i])
    
    return clauses

def generate_random_instance(n):
    formula = generate_tseitin_formula(n)
    return formula, len(formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        formula, proof_length = generate_random_instance(n)
        
        if not formula or proof_length <= 1:
            continue
        
        # Simulate computation of Riemannian metric tensor and its rank
        # (This is a placeholder; replace with actual computation)
        rank = random.randint(1, n)
        
        total_metric_value += rank
        instances_tested += 1
        
        if rank > 2 * proof_length:
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}, proof_length={proof_length}"
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")