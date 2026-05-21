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
    
    def generate_3xor_instance(n, alpha):
        m = int(alpha * n)
        clauses = []
        for _ in range(m):
            clause = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
            while len(set(clause)) < 2:
                clause[random.randint(0, 2)] = random.randint(0, 1)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def evaluate_instance(instance, assignment):
        return sum(all(assignment[i] == c for i in clause) for clause in instance)
    
    def compute_LW(instance, alpha):
        n = len(instance[0])
        tau = 1 - 1 / (8 * alpha)
        S_tau = {tuple(sorted([assignment[i] if i != j else 1 - assignment[j] for j in range(n)])) for assignment in product([0, 1], repeat=n) if evaluate_instance(instance, assignment) >= tau * len(instance)}
        LW = sum(math.log2(len(set(tuple(sorted([x[i] if i != j else 1 - x[j] for j in range(n)])) for x in S_tau))) / (n - 1) for i in range(n))
        return LW / n
    
    def product(iterables):
        pools = [tuple(pool) for pool in iterables]
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)
    
    n_values = [14, 16, 18, 20]
    alpha_values = [0.5, 0.7, 0.85, 0.918, 1.00, 1.10, 1.50]
    instances_tested = 0
    total_LW = 0
    
    for n in n_values:
        for alpha in alpha_values:
            instance = generate_3xor_instance(n, alpha)
            LW = compute_LW(instance, alpha)
            total_LW += LW
            instances_tested += 1
    
    mean_LW = total_LW / instances_tested
    if any(LW >= 0.02 for LW in [compute_LW(generate_3xor_instance(n, alpha), alpha) for n in n_values for alpha in [0.5, 0.7, 0.85]]):
        conjecture_holds = False
        counterexample = "LW >= 0.02 at α ≤ 0.85"
    elif any(LW <= 0.05 for LW in [compute_LW(generate_3xor_instance(n, alpha), alpha) for n in n_values for alpha in [1.10, 1.50]]):
        conjecture_holds = False
        counterexample = "LW <= 0.05 at α ≥ 1.10"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "LW",
        "metric_value": mean_LW,
        "instances_tested": instances_tested,
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
    
    mean_LW = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_LW} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")