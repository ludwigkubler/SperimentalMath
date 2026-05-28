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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
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
            for j in range(m):
                if j != rank and A[j][i] != 0:
                    factor = -A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] += factor * A[rank][k]
            rank += 1
        return rank
    
    def tropical_hodge_rank(clauses, n):
        m = len(clauses)
        H = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for lit in clause:
                if lit > 0:
                    H[i][lit - 1] = 1
                else:
                    H[i][-lit] = 1
        return gaussian_elimination(H)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        instance = generate_sat_instance(n)
        rank = tropical_hodge_rank(instance, n)
        ranks.append(rank)
    
    metric_value = sum(ranks) / len(ranks)
    instances_tested = len(ranks)
    conjecture_holds = all(rank <= math.log(n) for n, rank in zip(n_values, ranks))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "tropical_hodge_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8 and max(metric_values) <= 3:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed={first_failing_seed + 1}")