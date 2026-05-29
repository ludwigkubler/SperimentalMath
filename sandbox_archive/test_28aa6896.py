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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rref = gaussian_elimination(matrix)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def generate_cnf(n, m):
    cnf = []
    variables = list(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(variables, 2)
        cnf.append(clause)
    return cnf

def algebra_generated_by_cnf(cnf):
    n = len(cnf[0])
    algebra = []
    for assignment in itertools.product([0, 1], repeat=n):
        row = [1]
        for lit in range(1, n + 1):
            if assignment[lit - 1] == 1:
                row.append(lit)
            else:
                row.append(-lit)
        algebra.append(row)
    return algebra

def frege_proof_depth(cnf):
    # Placeholder function to simulate Frege proof depth
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(5, 20)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 20, 40]
    results = []
    
    for n in n_values:
        m = random.randint(n, 2 * n)
        cnf = generate_cnf(n, m)
        algebra_A = algebra_generated_by_cnf(cnf)
        algebra_B = algebra_generated_by_cnf(cnf)  # B_F is the same as A_F for simplicity
        
        tensor_product = []
        for row_A in algebra_A:
            for row_B in algebra_B:
                new_row = [1]
                for lit_A in row_A[1:]:
                    if lit_A > 0:
                        new_row.append(lit_A)
                    else:
                        new_row.append(-lit_A)
                for lit_B in row_B[1:]:
                    if lit_B > 0:
                        new_row.append(lit_B)
                    else:
                        new_row.append(-lit_B)
                tensor_product.append(new_row)
        
        rank_value = rank(tensor_product)
        proof_depth = frege_proof_depth(cnf)
        results.append((rank_value, proof_depth))
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ranks = [r for r, _ in results]
    depths = [d for _, d in results]
    
    def spearman_rank_correlation(ranks, depths):
        n = len(ranks)
        rank_diffs_squared = sum((ranks[i] - depths[i]) ** 2 for i in range(n))
        return 1 - (6 * rank_diffs_squared) / (n * (n**2 - 1))
    
    correlation_coefficient = spearman_rank_correlation(ranks, depths)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] or r["metric_value"] is None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")