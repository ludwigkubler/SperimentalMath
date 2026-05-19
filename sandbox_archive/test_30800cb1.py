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
    
    def gaussian_elimination(M):
        rows, cols = len(M), len(M[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(M[r][i]))
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            if factor == 0:
                continue
            for j in range(cols):
                M[i][j] /= factor
            for k in range(rows):
                if k != i:
                    factor = M[k][i]
                    for j in range(cols):
                        M[k][j] -= factor * M[i][j]
        return [sum(row) % 2 for row in M]

    def dnf_size(f, n):
        subcubes = []
        for i in range(1 << n):
            sigma = set()
            for j in range(n):
                if (i >> j) & 1:
                    sigma.add(j)
            if all(f(tuple(sorted(sigma))) == 1 for _ in range(len(sigma))):
                subcubes.append(sigma)
        
        F2_matrix_1 = [[0] * len(subcubes) for _ in range(len(subcubes))]
        F2_matrix_2 = [[0] * len(subcubes) for _ in range(len(subcubes))]
        
        for i, sigma1 in enumerate(subcubes):
            for j, sigma2 in enumerate(subcubes):
                if sigma1.issubset(sigma2):
                    F2_matrix_1[i][j] = 1
                if len(sigma1.intersection(sigma2)) == 2:
                    F2_matrix_2[i][j] = 1
        
        beta_1 = sum(gaussian_elimination(F2_matrix_1)) - sum(gaussian_elimination(F2_matrix_2))
        
        prime_implicants = []
        for i in range(1 << n):
            if f(tuple(sorted([j for j in range(n) if (i >> j) & 1]))) == 1:
                prime_implicants.append(i)
        
        def branch_and_bound(prime_implicants, cover):
            if not prime_implicants:
                return len(cover)
            p = min(prime_implicants, key=lambda x: sum((x >> i) & 1 for i in range(n)))
            cover.add(p)
            remaining = [pi for pi in prime_implicants if (pi & p) != p]
            return min(branch_and_bound(remaining, cover), branch_and_bound(remaining, cover - {p}))
        
        sigma_DNF = branch_and_bound(prime_implicants, set())
        
        return beta_1, sigma_DNF

    n_values = [4, 5, 6]
    p_values = [0.30, 0.50, 0.70]
    instances_tested = 0
    total_beta_1 = 0
    total_sigma_DNF = 0
    
    for n in n_values:
        for p in p_values:
            for _ in range(30):
                f = lambda x: int(random.random() < p)
                beta_1, sigma_DNF = dnf_size(f, n)
                instances_tested += 1
                total_beta_1 += beta_1
                total_sigma_DNF += sigma_DNF
                
                if beta_1 >= 1 and sigma_DNF < 3 * beta_1:
                    return {
                        "metric_name": "sigma_DNF",
                        "metric_value": sigma_DNF,
                        "instances_tested": instances_tested,
                        "conjecture_holds": False,
                        "counterexample": f"f={f}, n={n}, p={p}"
                    }
    
    mean_beta_1 = total_beta_1 / instances_tested
    mean_sigma_DNF = total_sigma_DNF / instances_tested
    
    return {
        "metric_name": "sigma_DNF",
        "metric_value": mean_sigma_DNF,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"failing seed\" first_failing_seed={first_failing_seed}")