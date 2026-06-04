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
    
    def generate_cnf(n, C):
        clauses = []
        for _ in range(C):
            clause = [random.randint(1, n), random.randint(1, n)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), random.randint(1, n)]
            clauses.append(tuple(sorted(clause)))
        return clauses

    def density_matrix(cnf):
        n = max([max(clause) for clause in cnf])
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            i, j = clause
            M[i][j] += 1
            M[j][i] += 1
        return M

    def geometric_entanglement(M):
        n = len(M)
        trace = sum([M[i][i] for i in range(n)])
        det = determinant(M)
        if det == 0:
            return float('inf')
        return -math.log(det) / (2 * math.pi)

    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det

    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)

    C_values = [random.randint(1, min(n-1, 40)) for _ in range(30)]
    E_values = []
    
    for C in C_values:
        cnf = generate_cnf(20, C)
        M = density_matrix(cnf)
        E = geometric_entanglement(M)
        E_values.append(E)

    correlation_coefficient = pearson_correlation(C_values, E_values)
    mean_difference = sum(abs(e - c) for e, c in zip(E_values, C_values)) / len(E_values)
    
    return {
        "metric_name": "geometric_entanglement_and_clause_set_complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": 20,
        "conjecture_holds": correlation_coefficient > 0.8 and mean_difference <= 3,
        "counterexample": "" if correlation_coefficient > 0.8 and mean_difference <= 3 else f"correlation_coefficient={correlation_coefficient}, mean_difference={mean_difference}"
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")