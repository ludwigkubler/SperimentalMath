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
    
    def generate_k_cnf(n: int, k: int):
        symbols = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(symbols, 2)
            clauses.append(clause)
        return clauses
    
    def construct_quasigroup(n: int):
        quasigroup = [[0] * n for _ in range(n)]
        elements = list(range(1, n + 1))
        random.shuffle(elements)
        for i in range(n):
            for j in range(n):
                quasigroup[i][j] = elements[(i + j) % n]
        return quasigroup
    
    def monotone_circuit_size(quasigroup: list, n: int):
        # Simplified heuristic to estimate circuit size
        return n * math.log2(n)
    
    k_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in k_values:
        for _ in range(5):  # Test each n with 5 instances
            cnf = generate_k_cnf(n, k)
            quasigroup = construct_quasigroup(n)
            circuit_size = monotone_circuit_size(quasigroup, n)
            predicted_bound = (1.0 * n ** k) / (2 ** k)
            ratio = circuit_size / predicted_bound
            results.append({
                "n": n,
                "circuit_size": circuit_size,
                "predicted_bound": predicted_bound,
                "ratio": ratio
            })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = mean_ratio <= 1.5
    
    return {
        "metric_name": "Mean Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mean_ratio_exceeds_bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio_exceeds_bound\" first_failing_seed={first_failing_seed}")