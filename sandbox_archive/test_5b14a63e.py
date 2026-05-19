# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(M):
    rows, cols = len(M), len(M[0])
    rank = 0
    for j in range(cols):
        pivot_row = None
        for i in range(rank, rows):
            if M[i][j] != 0:
                pivot_row = i
                break
        if pivot_row is None:
            continue
        M[pivot_row], M[rank] = M[rank], M[pivot_row]
        rank += 1
        for i in range(rank, rows):
            factor = -M[i][j] / M[rank-1][j]
            for k in range(cols):
                if j <= k:
                    M[i][k] += factor * M[rank-1][k]
    return rank

def dnf_size(f, n):
    subcubes = []
    for i in range(2**n):
        cube = [i >> j & 1 for j in range(n)]
        if all(f(tuple(cube)) == 1):
            subcubes.append(cube)
    
    F2_matrix_1 = [[0] * len(subcubes) for _ in range(len(subcubes))]
    F2_matrix_2 = [[0] * len(subcubes) for _ in range(len(subcubes))]
    
    for i, cube1 in enumerate(subcubes):
        for j, cube2 in enumerate(subcubes):
            if all(cube1[k] & cube2[k] == 0 for k in range(n)):
                F2_matrix_1[i][j] = 1
            if all(cube1[k] | cube2[k] == 1 for k in range(n)):
                F2_matrix_2[i][j] = 1
    
    beta_1 = sum(gaussian_elimination(F2_matrix_1)) - sum(gaussian_elimination(F2_matrix_2))
    
    def quine_mccluskey(f, n):
        minterms = [i for i in range(2**n) if f(tuple(i.to_bytes(n, 'big')))]
        prime_implicants = []
        essential_prime_implicants = []
        
        while True:
            implicants = []
            for term1 in minterms:
                covered = False
                for term2 in minterms:
                    if term1 != term2 and all((term1 >> i) & 1 == (term2 >> i) & 1 for i in range(n)):
                        covered = True
                        break
                if not covered:
                    implicants.append(term1)
            prime_implicants.extend(implicants)
            minterms = [term for term in minterms if any(all((term >> i) & 1 == (implicant >> i) & 1 for i in range(n)) for implicant in implicants)]
            if not minterms:
                break
        
        return len(prime_implicants)
    
    sigma_DNF = quine_mccluskey(f, n)
    
    return beta_1, sigma_DNF

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 5, 6]
    p_values = [0.3, 0.5, 0.7]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for p in p_values:
            f = lambda x: random.choices([0, 1], [1-p, p])[0]  # Random Boolean function
            beta_1, sigma_DNF = dnf_size(f, n)
            instances_tested += 1
            if beta_1 >= 1 and sigma_DNF < 3 * beta_1:
                conjecture_holds = False
                counterexample = f"f={f}, n={n}, p={p}"
    
    return {
        "metric_name": "sigma_DNF",
        "metric_value": sigma_DNF,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")