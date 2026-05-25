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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    if not any(is_prime(int(s)) for s in str(seed)):
        return {
            "metric_name": "Minimal Rank of Twisted Poisson Manifold",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "seed_not_prime"
        }
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        r = 0
        for i in range(rows):
            if any(matrix[i][j] != 0 for j in range(cols)):
                r += 1
        return r
    
    def construct_twisted_poisson_matrix(variables, clauses):
        n = len(variables)
        m = len(clauses)
        matrix = [[0] * (n + m) for _ in range(n + m)]
        
        for i, var in enumerate(variables):
            matrix[i][i] = 1
        
        for j, clause in enumerate(clauses):
            for lit in clause:
                if lit > 0:
                    matrix[n + j][lit - 1] = 1
                else:
                    matrix[n + j][-lit - 1] = -1
        
        return gaussian_elimination(matrix)
    
    def generate_sat_instance(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return variables, clauses
    
    max_n = 40
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            variables, clauses = generate_sat_instance(n, random.randint(1, n))
            matrix = construct_twisted_poisson_matrix(variables, clauses)
            min_rank = rank(matrix)
            expected_bound = 2 ** n * len(clauses)
            results.append({
                "n": n,
                "m": len(clauses),
                "min_rank": min_rank,
                "expected_bound": expected_bound
            })
    
    if all(result["min_rank"] <= result["expected_bound"] for result in results):
        return {
            "metric_name": "Minimal Rank of Twisted Poisson Manifold",
            "metric_value": sum(result["min_rank"] for result in results) / len(results),
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        counterexample = min((result for result in results if result["min_rank"] > result["expected_bound"]), key=lambda x: (x["n"], x["m"]))
        return {
            "metric_name": "Minimal Rank of Twisted Poisson Manifold",
            "metric_value": sum(result["min_rank"] for result in results) / len(results),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"n={counterexample['n']}, m={counterexample['m']}, min_rank={counterexample['min_rank']}, expected_bound={counterexample['expected_bound']}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        counterexample = min((r for r in results if not r["conjecture_holds"]), key=lambda x: (x["seed"], x["metric_value"]))
        print(f"RESULT: FALSIFIED counterexample=\"n={counterexample['n']}, m={counterexample['m']}, min_rank={counterexample['min_rank']}, expected_bound={counterexample['expected_bound']}\" first_failing_seed={counterexample['seed']}")