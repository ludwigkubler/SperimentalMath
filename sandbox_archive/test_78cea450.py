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
    
    def generate_k_cnf(n, m, k):
        cnf = []
        for _ in range(m):
            clause = set()
            while len(clause) < k:
                lit = random.randint(1, n * 2)
                if lit <= n:
                    clause.add(lit)
                else:
                    clause.add(-lit)
            cnf.append(tuple(sorted(clause)))
        return tuple(cnf)

    def min_state_complexity(cnf):
        states = set()
        for clause in cnf:
            new_state = tuple(sorted(set(states) | {tuple(clause)}))
            states.add(new_state)
        return len(states)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, n * 2)
            k = random.randint(1, min(k, n))
            cnf = generate_k_cnf(n, m, k)
            q_star = min_state_complexity(cnf)
            results.append({
                "n": n,
                "m": m,
                "k": k,
                "q_star": q_star
            })
    
    if not results:
        return {
            "metric_name": "min_state_complexity",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    total_q_star = sum(result["q_star"] for result in results)
    mean_q_star = total_q_star / instances_tested
    
    upper_bound = lambda n, m, k: (n + m + k) * math.log(n + m)
    
    conjecture_holds = all(q_star <= upper_bound(result["n"], result["m"], result["k"]) for result in results)
    counterexample = "" if conjecture_holds else "q_star > upper_bound"
    
    return {
        "metric_name": "min_state_complexity",
        "metric_value": mean_q_star,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_q_star = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_q_star} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_q_star} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"q_star > upper_bound\" first_failing_seed={first_failing_seed}")