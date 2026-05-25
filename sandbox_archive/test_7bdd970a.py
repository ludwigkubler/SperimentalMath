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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        max_comm = 0
        for i in range(2**(n-1)):
            x = bin(i)[2:].zfill(n-1)
            y = bin(i + (1 << (n-1)))[2:].zfill(n-1)
            comm = sum(abs(int(x[i]) - int(y[i])) for i in range(n-1))
            max_comm = max(max_comm, comm)
        return max_comm
    
    def tropical_hermitian_form(f):
        n = len(f)
        H = [[0] * n for _ in range(n)]
        for i in range(2**n):
            x = bin(i)[2:].zfill(n)
            y = bin(i + 1)[2:].zfill(n)
            value = sum(abs(int(x[i]) - int(y[i])) for i in range(n))
            H[int(x, 2)][int(y, 2)] = value
        return H
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = next(j for j in range(i, n) if matrix[j][i] != 0)
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            rank += 1
            for j in range(n):
                if i == j:
                    continue
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        C_f = communication_complexity(f)
        if C_f > n**(1/4):
            H = tropical_hermitian_form(f)
            rank = min_rank(H)
            total_rank += rank
            instances_tested += 1
    
    metric_value = total_rank / instances_tested if instances_tested > 0 else 0
    conjecture_holds = metric_value >= math.sqrt(n_values[-1])
    counterexample = "" if conjecture_holds else "communication_complexity_not_met"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"communication_complexity_not_met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")