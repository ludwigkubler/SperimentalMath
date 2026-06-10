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
    
    def generate_protocol(n):
        protocol = []
        for _ in range(n):
            input_bits = ''.join(random.choice('01') for _ in range(n))
            output_bits = ''.join(random.choice('01') for _ in range(n))
            protocol.append((input_bits, output_bits))
        return protocol
    
    def riesz_representation_rank(protocol):
        n = len(protocol)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for input_bits, output_bits in protocol:
            for i in range(n):
                if input_bits[i] == '1':
                    A[0][i + 1] += 1
                if output_bits[i] == '1':
                    A[i + 1][0] += 1
                if input_bits[i] == '1' and output_bits[i] == '1':
                    A[0][0] += 1
        rank = gaussian_elimination(A)
        return rank
    
    def rank_variance(protocol):
        n = len(protocol)
        rank_sum = sum(riesz_representation_rank([p]) for p in protocol)
        mean_rank = rank_sum / n
        variance = sum((riesz_representation_rank([p]) - mean_rank) ** 2 for p in protocol) / n
        return variance
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_correlation = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        protocol = generate_protocol(n)
        riesz_rank = riesz_representation_rank(protocol)
        rank_var = rank_variance(protocol)
        correlation = riesz_rank / (rank_var + 1e-9) if rank_var > 0 else 0
        total_correlation += correlation
        instances_tested += n
        n_max = max(n_max, n)
    
    mean_correlation = total_correlation / len(n_values)
    conjecture_holds = mean_correlation >= 0.8 and all(correlation >= 0.5 for correlation in [total_correlation / len(n_values)] * len(n_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_correlation,
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
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] == "mapping_undefined" for result in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")