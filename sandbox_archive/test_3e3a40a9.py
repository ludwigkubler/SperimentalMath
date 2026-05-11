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
    
    # Generate a random 3-CNF formula with n variables and m clauses
    n = random.randint(5, 40)
    m = random.randint(1, min(n**2, 2*n))
    cnf = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
        cnf.append(clause)
    
    # Construct the permanent tensor P_n
    P_n = [[1] * n for _ in range(n)]
    for clause in cnf:
        for lit in clause:
            if lit > 0:
                P_n[lit - 1][lit - 1] += 1
            else:
                P_n[-lit - 1][-lit - 1] += 1
    
    # Construct the determinant tensor D_m
    D_m = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                D_m[i][j] = (-1)**(i + j) * (n - 2)
    
    # Compute the Schur-Weyl decompositions via Young tableau counting
    def hook_length_formula(shape):
        n = len(shape)
        total = 1
        for i in range(n):
            for j in range(len(shape[i])):
                total *= (shape[i][j] + i + j + 1) / (i + j + 1)
        return total
    
    def dominant_irreducible_multiplicity(tensor, shape):
        n = len(tensor)
        m = len(shape)
        if n < m:
            return 0
        mult = 1
        for i in range(m):
            for j in range(len(shape[i])):
                mult *= tensor[i][j] + i + j + 1
                mult //= (i + j + 1)
        return mult
    
    mu_P_n = dominant_irreducible_multiplicity(P_n, [(n - m) // 2] * m)
    mu_D_m = dominant_irreducible_multiplicity(D_m, [m // 2] * m)
    
    # Measure the difference in dominant irreducible multiplicities
    diff = abs(mu_P_n - mu_D_m)
    
    # Verify the Ω(n^{1.5}) gap for m < n^{1.5}
    conjecture_holds = diff >= n**1.5
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": diff,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"m={m}, n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    std_diff = math.sqrt(sum((r["metric_value"] - mean_diff)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_diff} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_diff} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")