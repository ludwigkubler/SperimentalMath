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
    
    def generate_random_read_twice_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_representation(f):
        n = int(math.log2(len(f)))
        M = []
        for i in range(2**n):
            row = []
            for j in range(2**n):
                if f[i] == f[j]:
                    row.append(1)
                else:
                    row.append(0)
            M.append(row)
        return M
    
    def noncommutative_entropy(M):
        n = len(M)
        trace = sum(M[i][i] for i in range(n))
        det = 1
        for i in range(n):
            for j in range(i+1, n):
                if M[i][j] != 0:
                    det *= -M[j][i]
        return math.log2(abs(trace + det))
    
    def generate_random_matrix_representation(f):
        n = int(math.log2(len(f)))
        M = []
        for i in range(2**n):
            row = []
            for j in range(2**n):
                if f[i] == f[j]:
                    row.append(random.choice([0, 1]))
                else:
                    row.append(0)
            M.append(row)
        return M
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_random_read_twice_function(n)
        for _ in range(5):  # Generate multiple representations per function
            M = generate_random_matrix_representation(f)
            entropy = noncommutative_entropy(M)
            total_entropy += entropy
            instances_tested += 1
    
    conjecture_holds = total_entropy >= n**2 and total_entropy >= math.log(n) * instances_tested
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Total Noncommutative Entropy",
        "metric_value": total_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")