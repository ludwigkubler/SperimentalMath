# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_function(n, p):
        return [random.choice([0, 1]) for _ in range(2**n)] if random.random() < p else [0] * (2**n)
    
    def is_subcube(f, cube):
        return all(f(tuple(sub)) == 1 for sub in product(*[range(bit) for bit in cube]))
    
    def cubical_boundary_matrix(n, K_f):
        m = len(K_f)
        boundary_matrix = [[0] * (m + n) for _ in range(m)]
        for i, cube in enumerate(K_f):
            for j in range(len(cube)):
                for subcube in product(*[range(bit) if k == j else [bit] for k, bit in enumerate(cube)]):
                    if is_subcube(f, subcube):
                        boundary_matrix[i][j + len(cube)] = 1
        return boundary_matrix
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            pivot_row = -1
            for i in range(rank, m):
                if matrix[i][j] == 1:
                    pivot_row = i
                    break
            if pivot_row != -1:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for i in range(m):
                    if i != rank - 1 and matrix[i][j] == 1:
                        for k in range(n):
                            matrix[i][k] ^= matrix[rank - 1][k]
        return rank
    
    def dnf_size(f, n):
        K_f = [tuple(sub) for sub in product(range(2), repeat=n) if is_subcube(f, sub)]
        beta_1 = gaussian_elimination(cubical_boundary_matrix(n, K_f))
        sigma_DNF = 0
        for cube in K_f:
            if all(f(tuple(sub)) == 1 for sub in product(*[range(bit) for bit in cube])):
                sigma_DNF += 2**len(cube)
        return beta_1, sigma_DNF
    
    def quine_mccluskey(f, n):
        minterms = [i for i in range(2**n) if f(i)]
        prime_implicants = []
        while minterms:
            essential = set()
            for term in minterms:
                if all(term & other == 0 for other in minterms if term != other):
                    essential.add(term)
            prime_implicants.extend(essential)
            new_minterms = set()
            for term in minterms:
                if not any(term & other == 0 for other in essential):
                    new_minterms.add(term)
            minterms = new_minterms
        return len(prime_implicants)
    
    n_values = [4, 5, 6]
    p_values = [0.30, 0.50, 0.70]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n, p in product(n_values, p_values):
        f = generate_random_function(n, p)
        beta_1, sigma_DNF = dnf_size(f, n)
        if beta_1 >= 1:
            instances_tested += 1
            if sigma_DNF < 3 * beta_1:
                conjecture_holds = False
                counterexample = f"n={n}, p={p}, seed={seed}"
    
    return {
        "metric_name": "sigma_DNF",
        "metric_value": sigma_DNF,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=seeds[0]) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")