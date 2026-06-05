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
    
    def term_overlap_matrix(cnf):
        n = len(cnf[0])
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i in clause:
                if i > 0:
                    matrix[i][i] += 1
                else:
                    matrix[-i][-i] += 1
        return matrix
    
    def alexander_brandt_index(matrix):
        n = len(matrix) - 1
        trace = sum(matrix[i][i] for i in range(1, n + 1))
        det = determinant(matrix)
        if det == 0:
            return None
        return trace / det
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def communication_complexity_rank_variance(cnf):
        n = len(cnf[0])
        rank_variances = []
        for _ in range(30):  # Sample 30 local-complexity distributions
            distribution = [random.randint(1, n) for _ in range(n)]
            rank = sum(distribution)
            rank_variances.append(rank ** 2)
        return sum(rank_variances) / len(rank_variances)
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    abis = []
    variances = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        matrix = term_overlap_matrix(cnf)
        abis.append(alexander_brandt_index(matrix))
        variances.append(communication_complexity_rank_variance(cnf))
    
    if None in abis:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    corr = correlation(abis, variances)
    return {
        "metric_name": "correlation",
        "metric_value": corr,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 100))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.8\" first_failing_seed={first_failing_seed}")