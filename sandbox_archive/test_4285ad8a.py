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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def hodge_dimension(cnf):
        n = len(cnf[0])
        A = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i, lit in enumerate(clause):
                if lit > 0:
                    A[i][lit - 1] += 1
                else:
                    A[i][-lit - 1] += 1
        rank = gaussian_elimination(A)
        return n - rank
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return n - i
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))

    def frege_width(cnf):
        n = len(cnf[0])
        rank = gaussian_elimination([[abs(lit) for lit in clause] for clause in cnf])
        return 2 ** (n - rank)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        dim_H = hodge_dimension(cnf)
        w_phi = frege_width(cnf)
        results.append((dim_H, w_phi))
    
    dim_H_values = [res[0] for res in results]
    w_phi_values = [res[1] ** 2 for res in results]
    correlation_coefficient = sum((dim_H_values[i] - mean(dim_H_values)) * (w_phi_values[i] - mean(w_phi_values)) for i in range(len(results))) / (len(results) * std_dev(dim_H_values) * std_dev(w_phi_values))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([len(cnf[0]) for cnf in results]),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient > 0.7 else "Correlation coefficient <= 0.5"
    }

def mean(values):
    return sum(values) / len(values)

def std_dev(values):
    avg = mean(values)
    return math.sqrt(sum((x - avg) ** 2 for x in values) / len(values))

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = mean([res["metric_value"] for res in results])
    std_dev_value = std_dev([res["metric_value"] for res in results])
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient <= 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")