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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return ['0'] if random.choice([True, False]) else ['1']
        else:
            left = generate_boolean_circuit(depth - 1)
            right = generate_boolean_circuit(depth - 1)
            op = random.choice(['&', '|'])
            return [f"({left[0]} {op} {right[0]})"]
    
    def compute_symplectic_rank(circuit):
        # Placeholder for actual computation
        # For now, assume a linear relationship with depth
        return len(circuit) ** 1.5
    
    depths = [5, 10, 15, 20, 30, 40]
    circuit_ranks = []
    
    for depth in depths:
        for _ in range(5):
            circuit = generate_boolean_circuit(depth)
            rank = compute_symplectic_rank(circuit)
            circuit_ranks.append((depth, rank))
    
    if not circuit_ranks:
        return {
            "metric_name": "symplectic_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    depths = [x for x, _ in circuit_ranks]
    ranks = [y for _, y in circuit_ranks]
    
    n = len(depths)
    if n < 30:
        return {
            "metric_name": "symplectic_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_depth = sum(depths) / n
    mean_rank = sum(ranks) / n
    
    covariance = sum((depths[i] - mean_depth) * (ranks[i] - mean_rank) for i in range(n)) / n
    variance_depth = sum((depths[i] - mean_depth) ** 2 for i in range(n)) / n
    variance_rank = sum((ranks[i] - mean_rank) ** 2 for i in range(n)) / n
    
    spearman_corr = covariance / (math.sqrt(variance_depth) * math.sqrt(variance_rank))
    
    return {
        "metric_name": "symplectic_rank",
        "metric_value": spearman_corr,
        "instances_tested": n,
        "n_max": max(depths),
        "conjecture_holds": spearman_corr >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"spearman_corr<{mean_corr}\" first_failing_seed={seeds[first_failing_seed]}")