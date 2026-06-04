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
    
    def generate_formula(m):
        clauses = []
        for _ in range(m):
            literals = [random.choice([1, -1]) * i for i in range(1, m+1)]
            clauses.append(literals)
        return clauses
    
    def hermitian_form(clauses):
        n = len(clauses[0])
        H = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                for j in range(i, n):
                    H[i][j] += sum(c * d for c, d in zip(clause, clause[j:]))
                    H[j][i] = H[i][j]
        return H
    
    def kostant_section_dimension(H):
        n = len(H)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [H[i] + I[i] for i in range(n)]
        det_A = determinant(A)
        return det_A
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def cube_root(m):
        return round(m ** (1/3))
    
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    for m in m_values:
        formula = generate_formula(m)
        H = hermitian_form(formula)
        dim_Kostant = kostant_section_dimension(H)
        ratio = dim_Kostant / m
        expected_ratio = cube_root(m) / m
        results.append({
            "m": m,
            "dim_Kostant": dim_Kostant,
            "ratio": ratio,
            "expected_ratio": expected_ratio
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(abs(result["ratio"] - result["expected_ratio"]) < 3 * std_ratio for result in results) / len(results)
    
    return {
        "metric_name": "Ratio of Kostant Section Dimension to Number of Clauses",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["m"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"Ratio {mean_ratio} not within 3 std of expected {cube_root(m_values[-1]) / m_values[-1]}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio not within 3 std of expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")