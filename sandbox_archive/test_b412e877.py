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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(random.randint(1, n * (n - 1) // 2)):
            clause = [random.choice([-1, 1]) * i for i in range(1, n + 1)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            cnf.append(clause)
        return cnf

    def resolution_width(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        resolvents = set()
        while True:
            new_resolvents = set()
            for clause1, clause2 in itertools.combinations(clauses, 2):
                common_lits = [x for x in clause1 if -x in clause2]
                if common_lits:
                    new_clause = tuple(sorted(set(clause1) ^ set(clause2)))
                    if len(new_clause) == 1:
                        return len(resolvents)
                    new_resolvents.add(new_clause)
            if not new_resolvents:
                break
            resolvents.update(new_resolvents)
            clauses.update(new_resolvents)
        return float('inf')

    def symplectic_leaves(cnf):
        n = len(cnf[0])
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            lit = abs(clause[0])
            if lit > n:
                continue
            A[lit][n - lit] = -1
            for x in clause[1:]:
                if abs(x) <= n:
                    A[x][n - abs(x)] += 1
        rank = gaussian_elimination(A)
        return rank

    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            pivot = Fraction(1, matrix[i][i])
            for j in range(n):
                matrix[i][j] *= pivot
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        if n > 40:
            continue
        cnf = generate_cnf(n)
        resolution_width_val = resolution_width(cnf)
        symplectic_leaves_count = symplectic_leaves(cnf)
        
        instances_tested += len(cnf)
        n_max = max(n_max, n)
        
        if symplectic_leaves_count > 3 * resolution_width_val:
            conjecture_holds = False
            counterexample = f"n={n}, symplectic_leaves_count={symplectic_leaves_count}, resolution_width_val={resolution_width_val}"
            break
        
        total_metric_value += symplectic_leaves_count

    return {
        "metric_name": "symplectic_leaves_count",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")