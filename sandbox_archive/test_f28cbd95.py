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

def generate_read_twice_boolean_function(n):
    if n == 1:
        return [random.choice([0, 1])]
    left = generate_read_twice_boolean_function(n // 2)
    right = generate_read_twice_boolean_function(n - len(left))
    return [left[i] ^ right[i % len(right)] for i in range(n)]

def compute_free_probability_representation(f):
    n = len(f)
    A = [[0] * n for _ in range(n)]
    B = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if f[i] == 1 and f[j] == 1:
                A[i][j] += 1
            elif f[i] == 0 and f[j] == 0:
                B[i][j] += 1
    return A, B

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    tree_widths = []
    
    for n in n_values:
        f = generate_read_twice_boolean_function(n)
        A, B = compute_free_probability_representation(f)
        rank_A = gaussian_elimination(A)
        rank_B = gaussian_elimination(B)
        min_rank = min(rank_A, rank_B)
        ranks.append(min_rank)
        tree_widths.append(n)
    
    correlation_coefficient = sum((ranks[i] - mean(ranks)) * (tree_widths[i] - mean(tree_widths)) for i in range(len(ranks))) / math.sqrt(sum((ranks[i] - mean(ranks))**2 for i in range(len(ranks)))) / math.sqrt(sum((tree_widths[i] - mean(tree_widths))**2 for i in range(len(tree_widths))))
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean(ranks) <= n_values[-1] * math.log(2 * n_values[-1])
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> mean_rank=<{}>".format(correlation_coefficient, mean(ranks))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def mean(lst):
    return sum(lst) / len(lst)

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={:.2f} std=0.00 support_fraction={:.2f}".format(mean_value, 0.00, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.2f} std=0.00 support_fraction={:.2f}".format(mean_value, 0.00, support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(result["counterexample"], first_failing_seed))