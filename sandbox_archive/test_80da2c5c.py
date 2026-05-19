# auto-injected by SEC sandbox
import math
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
from itertools import product, combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_subcube(f, sub):
        return all(f(tuple(sub)) == 1 for sub in product(*[range(bit + 1) for bit in sub]))
    
    def dnf_size(f, n):
        K_f = [tuple(sub) for sub in product(range(2), repeat=n) if is_subcube(f, sub)]
        beta_1 = compute_beta_1(K_f)
        sigma_DNF = compute_sigma_DNF(f, n)
        return beta_1, sigma_DNF
    
    def compute_beta_1(K_f):
        n = len(K_f[0])
        F2_matrix = [[0] * (2 ** n) for _ in range(2 ** n)]
        for i, subcube in enumerate(K_f):
            for j in range(n):
                new_subcube = list(subcube)
                new_subcube[j] = 1 - new_subcube[j]
                F2_matrix[i][K_f.index(tuple(new_subcube))] = 1
        return gaussian_elimination(F2_matrix, n)
    
    def gaussian_elimination(matrix, n):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if matrix[row][col] == 1:
                    pivot_row = row
                    break
            if pivot_row != -1:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for row in range(rows):
                    if row != rank - 1 and matrix[row][col] == 1:
                        matrix[row] = [matrix[row][i] ^ matrix[rank - 1][i] for i in range(cols)]
        return cols - rank
    
    def compute_sigma_DNF(f, n):
        prime_implicants = []
        for subcube in product(range(2), repeat=n):
            if f(subcube) == 1:
                prime_implicants.append(subcube)
        cover = set()
        for implicant in prime_implicants:
            uncovered = [i for i in range(n) if any(implicant[i] != cube[i] for cube in cover)]
            if not uncovered:
                continue
            min_cover = []
            for bit in uncovered:
                new_cover = cover.copy()
                new_cover.add(bit)
                min_cover.append(new_cover)
            cover = min(min_cover, key=len)
        return len(cover)
    
    n_values = [4, 5, 6]
    p_values = [0.30, 0.50, 0.70]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for p in p_values:
            for _ in range(30):
                f = lambda x: random.choices([0, 1], [1 - p, p])[0]
                beta_1, sigma_DNF = dnf_size(f, n)
                if beta_1 >= 1 and sigma_DNF < 3 * beta_1:
                    conjecture_holds = False
                    counterexample = f"f with n={n}, p={p}"
                    break
            instances_tested += 30
    
    return {
        "metric_name": "sigma_DNF",
        "metric_value": 3 * compute_beta_1(K_f),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")