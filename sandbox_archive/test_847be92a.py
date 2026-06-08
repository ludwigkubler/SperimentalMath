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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def compute_clause_depth(cnf):
        return max(len(clause) for clause in cnf)
    
    def compute_aos_complexity(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        matroid_basis = []
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if all(any(lit == -i or lit == -j for lit in clause) for clause in cnf):
                    matroid_basis.append([i, j])
        return len(matroid_basis)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if rank >= m:
                break
            pivot_row = rank
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == m:
                    pivot_row -= 1
                    break
            matrix[rank], matrix[pivot_row] = matrix[pivot_row], matrix[rank]
            for j in range(n):
                if i != j and matrix[rank][j] != 0:
                    factor = Fraction(matrix[j][i], matrix[rank][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def compute_rank(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        matrix = [[0] * (n + 1) for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    matrix[lit - 1][lit] += 1
                else:
                    matrix[-lit - 1][-lit] += 1
        return gaussian_elimination(matrix)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    cnf = generate_cnf(n, m)
    cd = compute_clause_depth(cnf)
    aos = compute_aos_complexity(cnf)
    
    return {
        "metric_name": "AOS vs CD",
        "metric_value": aos / cd,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": aos > cd,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"AOS <= CD\" first_failing_seed={first_failing_seed}")