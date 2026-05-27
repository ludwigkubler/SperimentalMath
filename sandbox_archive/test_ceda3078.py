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
    
    def xor_and_tree_width(n):
        if n == 1:
            return 1
        else:
            return 2 * xor_and_tree_width(n - 1)
    
    def frobenius_norm(matrix):
        sum_of_squares = sum(sum(x**2 for x in row) for row in matrix)
        return math.sqrt(sum_of_squares)
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        if n == 1:
            return [matrix[0][0]]
        else:
            det = 0
            for j in range(n):
                sub_matrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
                det += (-1)**j * matrix[0][j] * characteristic_polynomial(sub_matrix)
            return [det]
    
    def min_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for r in range(rows):
            if any(matrix[r][c] != 0 for c in range(cols)):
                rank += 1
                for c in range(cols):
                    matrix[r][c] /= matrix[r][r]
                for i in range(rows):
                    if i != r:
                        factor = matrix[i][r]
                        for j in range(cols):
                            matrix[i][j] -= factor * matrix[r][j]
        return rank
    
    def log_n(f, n):
        result = f
        for _ in range(n):
            result = math.log(result)
        return result
    
    n = random.randint(5, 40)
    f = random.random()
    w = xor_and_tree_width(n)
    matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    char_poly = characteristic_polynomial(matrix)
    frob_norm = frobenius_norm(char_poly)
    min_rank_val = min_rank(char_poly)
    
    log_w_f = log_n(f, w)
    upper_bound = w**(1/3) * log_w_f
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank_val,
        "instances_tested": 1,
        "conjecture_holds": min_rank_val <= upper_bound,
        "counterexample": "" if min_rank_val <= upper_bound else f"Counterexample: n={n}, w={w}, min_rank={min_rank_val}, upper_bound={upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")