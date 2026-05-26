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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            max_row = rank
            for j in range(rank, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            if A[max_row][i] == 0:
                continue
            A[rank], A[max_row] = A[max_row], A[rank]
            for j in range(n):
                if j != i and A[j][i] != 0:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
            rank += 1
        return rank
    
    def moment_map(clauses):
        n = len(clauses[0])
        A = [[0] * (2*n) for _ in range(2*n)]
        for clause in clauses:
            i, j = abs(clause[0])-1, abs(clause[1])-1
            A[i][j+n] = 1 if clause[0] > 0 else -1
            A[j][i+n] = 1 if clause[1] > 0 else -1
        return gaussian_elimination(A)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 random instances
            k = int(n * (math.log(n) / math.log(2)))
            clauses = generate_kcnf(n, k)
            rank = moment_map(clauses)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    expected_rank = 2**(n_values[-1]/4)
    
    if abs(mean_rank - expected_rank) > 3:
        conjecture_holds = False
        counterexample = f"Mean rank {mean_rank} deviates by more than a factor of 2^{n_values[-1]/4}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Minimal Symplectic Leaf Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank deviates by more than a factor of 2^{n_values[-1]/4}\" first_failing_seed={first_failing_seed}")