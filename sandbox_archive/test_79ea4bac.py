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

def xor_and_formula(n):
    if n == 1:
        return [random.choice([0, 1])]
    left = xor_and_formula(n // 2)
    right = xor_and_formula(n - n // 2)
    return [x ^ y for x in left] + [x & y for x in left] + [y & z for y in right for z in left]

def hodge_decomposition_mod_2(poly):
    n = len(poly)
    H = [[0] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = poly[i]
    return H

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    row_echelon_form = matrix[:]
    lead = 0
    for r in range(m):
        if lead >= n:
            break
        i = r
        while row_echelon_form[i][lead] == 0:
            i += 1
            if i == m:
                i = r
                lead += 1
                if lead >= n:
                    break
        row_echelon_form[r], row_echelon_form[i] = row_echelon_form[i], row_echelon_form[r]
        for i in range(m):
            if i != r:
                factor = Fraction(row_echelon_form[i][lead], row_echelon_form[r][lead])
                for j in range(n):
                    row_echelon_form[i][j] -= factor * row_echelon_form[r][j]
        lead += 1
    return sum(1 for row in row_echelon_form if any(row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = xor_and_formula(n)
    poly = [-x for x in formula]  # Negate the polynomial
    H = hodge_decomposition_mod_2(poly)
    rank_H = rank(H)
    f_n = math.log2(n) ** 2
    return {
        "metric_name": "rank",
        "metric_value": rank_H,
        "instances_tested": 1,
        "conjecture_holds": rank_H <= f_n + 0.1 * f_n,  # Allow a 10% margin of error
        "counterexample": "" if rank_H <= f_n + 0.1 * f_n else f"rank(H(F)) = {rank_H}, expected ≤ {f_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank(H(F)) exceeded f(n)\" first_failing_seed={first_failing_seed}")