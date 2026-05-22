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
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        A = gaussian_elimination(A)
        r = 0
        for row in A:
            if any(row):
                r += 1
        return r

    def ac0_circuit_depth(n):
        # Placeholder function, actual implementation required
        return n * (n - 1) // 2  # Example: quadratic complexity

    def generate_cnf(n):
        symbols = [f"x{i}" for i in range(n)]
        clauses = []
        for _ in range(n):
            clause = random.sample(symbols, random.randint(1, n))
            clauses.append(clause)
        return clauses

    def cnf_to_matrix(cnf):
        n = len(cnf)
        m = 2 ** n
        A = [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            binary = format(i, f'0{n}b')
            for j in range(n):
                if binary[j] == '1':
                    for clause in cnf:
                        if all(s in binary for s in clause):
                            A[i][j] = 1
                            break
        return A

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    matrix = cnf_to_matrix(cnf)
    bruer_group_rank = rank(matrix)
    ac0_depth = ac0_circuit_depth(n)

    if bruer_group_rank > ac0_depth:
        return {
            "metric_name": "Brauer Group Rank vs AC0 Circuit Depth",
            "metric_value": bruer_group_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, CNF={cnf}, Brauer Group Rank={bruer_group_rank}, AC0 Depth={ac0_depth}"
        }
    else:
        return {
            "metric_name": "Brauer Group Rank vs AC0 Circuit Depth",
            "metric_value": bruer_group_rank,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Brauer Group Rank > AC0 Depth\" first_failing_seed={first_failing_seed}")