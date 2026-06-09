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

def generate_cnf(n: int) -> list:
    cnf = []
    num_vars = n
    for _ in range(num_vars):
        clause = [random.randint(-1, -num_vars), random.randint(1, num_vars)]
        cnf.append(clause)
    return cnf

def power_iteration(matrix: list, iterations: int) -> float:
    n = len(matrix)
    v = [1.0 / math.sqrt(n)] * n
    for _ in range(iterations):
        v_next = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
        norm = sum(v_next[i]**2 for i in range(n))
        v = [v_next[i] / math.sqrt(norm) for i in range(n)]
    return abs(v[1])

def laplacian_matrix(cnf: list, n: int) -> list:
    adj_matrix = [[0] * n for _ in range(n)]
    for clause in cnf:
        for lit in clause:
            if lit > 0:
                i = lit - 1
            else:
                i = -lit - 1
            adj_matrix[i][i] += 1
    degree_sum = [sum(row) for row in adj_matrix]
    laplacian = [[degree_sum[i] - adj_matrix[i][j] if i == j else -adj_matrix[i][j] for j in range(n)] for i in range(n)]
    return laplacian

def resolution_width(cnf: list) -> int:
    stack = []
    literals = set()
    for clause in cnf:
        literals.update(clause)
    while literals:
        literal = random.choice(list(literals))
        if literal > 0:
            literals.remove(-literal)
            for clause in cnf:
                if literal in clause:
                    clause.remove(literal)
                    if not clause:
                        return len(stack) + 1
                elif -literal in clause:
                    clause.remove(-literal)
                    stack.append((clause, literal))
        else:
            literals.remove(-literal)
            for clause in cnf:
                if -literal in clause:
                    clause.remove(-literal)
                    if not clause:
                        return len(stack) + 1
                elif literal in clause:
                    clause.remove(literal)
                    stack.append((clause, -literal))
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    laplacian = laplacian_matrix(cnf, n)
    eig2 = power_iteration(laplacian, 1000)
    width = resolution_width(cnf)
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": eig2 > 0 and width > 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")