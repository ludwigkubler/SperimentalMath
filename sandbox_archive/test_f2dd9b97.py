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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = set()
            while len(clause) < 2:
                var = random.randint(1, n)
                if var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses

    def deligne_lusztig_rank(clauses):
        n = max(max(clause) for clause in clauses)
        monomial_basis = [1] + [0] * (n ** 2 - 1)
        
        def matrix_mult(A, B):
            result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]
            return result
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(rows):
                if matrix[i][i] == 0:
                    for j in range(i + 1, rows):
                        if matrix[j][i] != 0:
                            matrix[i], matrix[j] = matrix[j], matrix[i]
                            break
                    else:
                        return None  # Singular matrix
                pivot = matrix[i][i]
                for j in range(cols):
                    matrix[i][j] /= pivot
                for j in range(rows):
                    if j != i:
                        factor = matrix[j][i]
                        for k in range(cols):
                            matrix[j][k] -= factor * matrix[i][k]
            return matrix
        
        def deligne_lusztig_action(monomial, clauses):
            result = 0
            for clause in clauses:
                product = 1
                for var in clause:
                    if var in monomial:
                        product *= -1
                result += product
            return result
        
        action_matrix = [[deligne_lusztig_action((i + 1, j + 1), clauses) for j in range(n)] for i in range(n)]
        rank_matrix = gaussian_elimination(action_matrix)
        if rank_matrix is None:
            return None  # Singular matrix
        rank = sum(1 for row in rank_matrix if any(row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        k = random.randint(1, min(n - 1, 10))
        formula = generate_k_cnf(n, k)
        rank = deligne_lusztig_rank(formula)
        if rank is not None:
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_rank >= n_values[-1] ** 0.5 + 1e-6
    counterexample = "" if conjecture_holds else f"Formula with rank {mean_rank} < {n_values[-1]}^0.5"
    
    return {
        "metric_name": "Deligne-Lusztig Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")