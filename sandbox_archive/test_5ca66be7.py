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
    
    def generate_protocol(n):
        protocol = []
        for _ in range(n):
            input_bits = ''.join(random.choice('01') for _ in range(n))
            output_bits = ''.join(random.choice('01') for _ in range(n))
            protocol.append((input_bits, output_bits))
        return protocol
    
    def compute_matrix(protocol):
        n = len(protocol)
        matrix = [[0] * n for _ in range(n)]
        for i, (input_bits, output_bits) in enumerate(protocol):
            for j, (input_bits2, output_bits2) in enumerate(protocol):
                if input_bits == input_bits2 and output_bits != output_bits2:
                    matrix[i][j] = 1
        return matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            rank += 1
            for j in range(i+1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def compute_rank_variance(matrix):
        n = len(matrix)
        rank = gaussian_elimination(matrix)
        variance = 0
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] != 0:
                    variance += (matrix[i][j] ** 2) * (n - rank)
        return variance
    
    def compute_riesz_representation_rank(protocol):
        matrix = compute_matrix(protocol)
        return gaussian_elimination(matrix)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        protocol = generate_protocol(n)
        rrr = compute_riesz_representation_rank(protocol)
        rv = compute_rank_variance(matrix)
        results.append((n, rrr, rv))
    
    correlation_sum = 0
    instances_tested = 0
    n_max = max(n for _, _, _ in results)
    for n, rrr, rv in results:
        if rv == 0:
            continue
        instances_tested += 1
        correlation_sum += (rrr - Fraction(1, 2)) * (rv - Fraction(1, 2))
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = Fraction(correlation_sum, instances_tested)
    return {
        "metric_name": "correlation",
        "metric_value": float(correlation),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.8 and all(corr >= 0.5 for _, corr in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")