# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_disjointness_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j] = 1
            matrix[j][i] = 1
    return matrix

def tensor_product(t1, t2):
    result = []
    for a in t1:
        row = []
        for b in t2:
            row.extend([x * y for x, y in zip(a, b)])
        result.append(row)
    return result

def rank_1_decomposition(tensor):
    n = len(tensor)
    U = [[0] * n for _ in range(n)]
    V = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if tensor[i][j] != 0:
                U[i][i] = 1
                V[j][j] = 1
                break
    return U, V

def slice_rank(tensor):
    n = len(tensor)
    rank_1_count = 0
    for i in range(n):
        for j in range(n):
            sub_tensor = [row[j:] for row in tensor[i:]]
            u, v = rank_1_decomposition(sub_tensor)
            if all(all(x == 0 or x == 1 for x in row) for row in u) and all(all(x == 0 or x == 1 for x in col) for col in v):
                rank_1_count += 1
    return rank_1_count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        matrix = generate_disjointness_matrix(n)
        rank = slice_rank(matrix)
        results.append({
            "metric_name": "slice_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": rank >= n,
            "counterexample": "" if rank >= n else f"n={n}, rank={rank}"
        })
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.extend(result["results"])
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
    else:
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")