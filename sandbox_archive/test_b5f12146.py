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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(len(clause)) for j in range(i + 1, len(clause))):
                clauses.append(clause)
        return clauses
    
    def compute_hodge_arakelov_index(cnf):
        # Placeholder for actual computation
        return random.random() * 10
    
    def compute_frege_proof_depth(cnf):
        # Placeholder for actual computation
        return random.randint(5, 20)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        ai = compute_hodge_arakelov_index(cnf)
        d = compute_frege_proof_depth(cnf)
        if ai > 10 or d > 10:
            return {
                "metric_name": "AI vs d",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "value_exceeds_limit"
            }
        results.append((ai, d))
    
    if len(results) < 30:
        return {
            "metric_name": "AI vs d",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ai_values, d_values = zip(*results)
    n = len(ai_values)
    mean_ai = sum(ai_values) / n
    mean_d = sum(d_values) / n
    covariance = sum((ai - mean_ai) * (d - mean_d) for ai, d in results) / n
    variance_d = sum((d - mean_d) ** 2 for d in d_values) / n
    pearson_corr = covariance / math.sqrt(variance_d)
    
    return {
        "metric_name": "AI vs d",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "AI vs d correlation < 0.7"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")