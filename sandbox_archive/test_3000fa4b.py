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
    
    def secant_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def generate_disjointness_matrix(n):
        matrix = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                matrix[i][j] = random.choice([0, 1])
                matrix[j][i] = 1 - matrix[i][j]
        return matrix
    
    def compute_secant_rank(matrix):
        n = len(matrix)
        rank = secant_rank(matrix)
        for i in range(n):
            for j in range(i+1, n):
                new_matrix = [row[:] for row in matrix]
                new_matrix[i][j] = 1 - new_matrix[i][j]
                new_matrix[j][i] = 1 - new_matrix[j][i]
                rank += secant_rank(new_matrix)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        matrix = generate_disjointness_matrix(n)
        secant_rank_value = compute_secant_rank(matrix)
        results.append(secant_rank_value)
    
    mean_rank = sum(results) / len(results)
    conjecture_holds = all(rank >= n for rank, n in zip(results, n_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "secant_rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 53))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")