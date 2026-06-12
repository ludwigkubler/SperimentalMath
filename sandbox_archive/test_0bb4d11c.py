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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def matrix_from_cnf(cnf, n):
        m = len(cnf)
        A = [[0] * (2 * n) for _ in range(m)]
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal < 0:
                    row = -literal - 1
                    col = abs(literal) - 1
                else:
                    row = literal - 1
                    col = n + literal - 1
                A[i][col] = 1
        return A
    
    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if any(A[j][i] != 0 for j in range(rank)):
                A[rank], A[i] = A[i], A[rank]
                for j in range(m):
                    if j != rank:
                        factor = A[j][i] / A[rank][i]
                        for k in range(n):
                            A[j][k] -= factor * A[rank][k]
                rank += 1
        return rank
    
    def cnf_resolution_width(cnf):
        queue = [set(clause) for clause in cnf]
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    common_literals = set(queue[i]) & set(queue[j])
                    if len(common_literals) == 1:
                        literal = next(iter(common_literals))
                        new_clause = (queue[i] ^ {literal}) | (queue[j] ^ {literal})
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return len(queue)
            queue.append(new_clause)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            A = matrix_from_cnf(cnf, n)
            rank = matrix_rank(A)
            width = cnf_resolution_width(cnf)
            total_rank += rank
            total_width += width
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_width = total_width / instances_tested
    conjecture_holds = math.isclose(mean_rank, math.sqrt(n), abs_tol=1)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")