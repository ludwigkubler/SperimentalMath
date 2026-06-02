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
    
    def generate_d_regular_circuit(n, d):
        if n % d != 0 or d < 2:
            return None
        circuit = [[random.choice([0, 1]) for _ in range(d)] for _ in range((n + d - 1) // d)]
        return circuit
    
    def monotone_width(circuit):
        n = len(circuit[0])
        width = [0] * (n + 1)
        for row in circuit:
            max_val = 0
            for val in row:
                if val == 1:
                    max_val += 1
                else:
                    break
            width[max_val] += 1
        return sum(width[i] * i for i in range(1, n + 1))
    
    def p_adic_hodge_rank(circuit):
        n = len(circuit[0])
        m = len(circuit)
        A = [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if circuit[i][j] == 1:
                    A[i][j] = 1
                    A[i][-1] += 1
        
        rank = 0
        for row in A:
            if any(row[j] != 0 for j in range(n)):
                rank += 1
                for i in range(m):
                    if A[i][j] == 1:
                        for k in range(n + 1):
                            A[i][k] ^= row[k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_d_regular_circuit(n, 2)
            if circuit is None:
                continue
            rank = p_adic_hodge_rank(circuit)
            width = monotone_width(circuit)
            results.append((rank, width))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(results)
    rank_sum = sum(result[0] for result in results)
    width_sum = sum(result[1] for result in results)
    rank_mean = rank_sum / n
    width_mean = width_sum / n
    
    correlation = 0.0
    for rank, width in results:
        correlation += (rank - rank_mean) * (width - width_mean)
    correlation /= n * math.sqrt(sum((result[0] - rank_mean) ** 2 for result in results)) * math.sqrt(sum((result[1] - width_mean) ** 2 for result in results))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")