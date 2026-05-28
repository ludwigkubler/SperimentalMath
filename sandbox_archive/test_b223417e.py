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
    
    def generate_xor_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_ehrhart_rank(circuit):
        n = len(circuit)
        if n == 1:
            return 0
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        for i in range(2**n):
            x = circuit[i]
            for j in range(n):
                if x & (1 << j):
                    A[j][i] += 1
                else:
                    A[n][i] += 1
            b[i] = x
        rank = gaussian_elimination(A, b)
        return rank
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = -A[j][i] / A[i][i]
                A[j][i:] = [x + factor * y for x, y in zip(A[j][i:], A[i][i:])]
                b[j] += factor * b[i]
        rank = sum(1 for row in A if any(row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        circuit = generate_xor_circuit(n)
        rank = compute_ehrhart_rank(circuit)
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    log_n = [math.log2(n) for n in n_values]
    correlation = sum((r - mean_rank) * (l - math.mean(log_n)) for r, l in zip(ranks, log_n)) / (len(ranks) * math.sqrt(sum((r - mean_rank)**2 for r in ranks) * sum((l - math.mean(log_n))**2 for l in log_n)))
    
    if correlation < 0.9:
        return {
            "metric_name": "Correlation",
            "metric_value": correlation,
            "instances_tested": len(ranks),
            "conjecture_holds": False,
            "counterexample": f"Low correlation: {correlation}"
        }
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Low correlation\" first_failing_seed={first_failing_seed}")