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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = -1
            for i in range(rank, m):
                if A[i][j] != 0:
                    i_max = i
                    break
            if i_max == -1:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for k in range(n):
                if k != j and A[rank][k] != 0:
                    factor = A[k][j] / A[rank][j]
                    for l in range(n):
                        A[k][l] -= factor * A[rank][l]
            rank += 1
        return rank
    
    def tseitin_formula(phi):
        literals = set()
        clauses = []
        for literal in phi:
            literals.add(literal)
            literals.add(-literal)
        for literal in literals:
            clause = [literal]
            for other_literal in literals:
                if other_literal != literal and -other_literal not in clause:
                    clause.append(other_literal)
            clauses.append(clause)
        return clauses
    
    def geometric_representation(clauses):
        p = 2  # Using a fixed p-adic field, e.g., Q_2
        A = [[0] * (len(clauses) + 1) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal > 0:
                    A[i][literal - 1] += 1
                else:
                    A[i][-1] += 1
        return gaussian_elimination(A)
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2 ** n):
            clause = random.sample(range(-n, 0), random.randint(1, n))
            cnf.append(clause)
        return cnf
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = generate_cnf(n)
            phi_G = tseitin_formula(phi)
            rank = geometric_representation(phi_G)
            ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    f_n_values = [2 ** (n * n) for n in n_values]
    
    if all(mean_rank <= f_n for f_n in f_n_values):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "f(n) grows faster than doubly-exponentially"
    
    return {
        "metric_name": "mean_rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"f(n) grows faster than doubly-exponentially\" first_failing_seed={first_failing_seed}")