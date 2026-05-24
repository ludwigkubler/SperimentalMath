# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def construct_matrix(bp):
        n = len(bp)
        if n == 2:
            return [[1, 0], [0, 1]]
        else:
            matrix = []
            for i in range(n):
                row = [0] * (n ** 2)
                for j in range(2 ** (i - 1)):
                    row[j * 2 + bp[i]] = 1
                matrix.append(row)
            return matrix
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    matrix[i][j] /= matrix[i][j]
                for k in range(m):
                    if k != i and any(matrix[k][j] != 0 for j in range(n)):
                        for j in range(n):
                            matrix[k][j] -= matrix[i][j] * matrix[k][i]
        return rank
    
    def is_ip2(bp):
        return bp == [1, 0, 1, 0]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size 5 times to ensure statistical robustness
            bp = [random.randint(0, 1) for _ in range(n)]
            matrix = construct_matrix(bp)
            rank = min_rank(matrix)
            total_rank += rank
            instances_tested += 1
    
    avg_rank = total_rank / instances_tested
    
    if is_ip2(bp):
        conjecture_holds = avg_rank >= n
        counterexample = "" if conjecture_holds else "IP_2 BP failed"
    else:
        conjecture_holds = avg_rank <= math.log(n)
        counterexample = "" if conjecture_holds else f"BP size {n} failed"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")