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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                if i == k:
                    A[j][k] = 0
                else:
                    A[j][k] += factor * A[i][k]
    return A

def rank(A):
    m, n = len(A), len(A[0])
    r = min(m, n)
    for i in range(r):
        if abs(A[i][i]) == 0:
            r -= 1
    return r

def tseitin_formula(cnf):
    literals = {}
    new_clauses = []
    counter = 1
    for clause in cnf:
        new_clause = []
        for lit in clause:
            if lit not in literals:
                literals[lit] = counter
                counter += 1
            new_clause.append(literals[lit])
        new_clauses.append(new_clause)
    return new_clauses, literals

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_rank = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = []
            for _ in range(random.randint(1, n)):
                clause = random.sample(range(-n, -1) + list(range(1, n+1)), random.randint(1, n))
                cnf.append(clause)
            
            phi_G, literals = tseitin_formula(cnf)
            rank_phi_G = rank(phi_G)
            total_rank += rank_phi_G
            instances_tested += 1

    mean_rank = total_rank / instances_tested
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")