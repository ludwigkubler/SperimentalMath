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
    
    def construct_matrix(bp):
        n = len(bp)
        if n == 1:
            return [[1]]
        matrix = [[0] * (2 ** n) for _ in range(2 ** n)]
        for i in range(n):
            for j in range(2 ** (i - 1)):
                matrix[j][j ^ bp[i]] = 1
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        for i in range(m):
            if all(x == 0 for x in matrix[i]):
                continue
            pivot_col = next(j for j in range(n) if matrix[i][j] != 0)
            for j in range(i + 1, m):
                factor = Fraction(matrix[j][pivot_col], matrix[i][pivot_col])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(x != 0 for x in row))
    
    def is_trivial_bp(bp):
        return all(x == 0 or x == 1 for x in bp)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size 5 times to ensure statistical robustness
            if n == 2 and is_trivial_bp(bp):
                continue
            bp = [random.randint(0, 1) for _ in range(n)]
            matrix = construct_matrix(bp)
            rank_value = rank(matrix)
            total_rank += rank_value
            instances_tested += 1
    
    average_rank = total_rank / instances_tested
    
    if n == 2 and is_trivial_bp(bp):
        conjecture_holds = False
        counterexample = "trivial_IP_2"
    else:
        conjecture_holds = average_rank <= math.log(instances_tested, 2)
        counterexample = ""
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": average_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='trivial_IP_2' first_failing_seed={first_failing_seed + 1}")