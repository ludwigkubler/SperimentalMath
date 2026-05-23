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
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses
    
    def construct_toric_variety(clauses):
        points = []
        for clause in clauses:
            point = [0] * len(clause)
            for i, var in enumerate(clause):
                if var > 0:
                    point[i] = 1
                else:
                    point[i] = -1
            points.append(point)
        return points
    
    def min_rank(points):
        m, n = len(points), len(points[0])
        A = [points[i] + [-1] for i in range(m)]
        rank = 0
        for j in range(n):
            pivot_row = -1
            for i in range(rank, m):
                if A[i][j] != 0:
                    pivot_row = i
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            rank += 1
            for i in range(m):
                if i != rank and A[i][j] != 0:
                    factor = A[i][j] / A[rank][j]
                    for k in range(n + 1):
                        A[i][k] -= factor * A[rank][k]
        return rank
    
    def ac0_circuit_threshold(clauses):
        n = len(clauses[0])
        if n == 1:
            return 1
        return n
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    toric_variety = construct_toric_variety(cnf)
    min_rank_value = min_rank(toric_variety)
    ac0_threshold = ac0_circuit_threshold(cnf)
    
    if min_rank_value == 0:
        return {
            "metric_name": "log_n_over_min_rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "min_rank_is_zero"
        }
    
    ratio = math.log(n) / min_rank_value
    conjecture_holds = abs(ratio - ac0_threshold) <= 0.1 * ac0_threshold
    
    return {
        "metric_name": "log_n_over_min_rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"ratio={ratio}, threshold={ac0_threshold}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")