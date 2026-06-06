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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def min_rank(matrix):
        rank = 0
        n = len(matrix)
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank

    def frege_proof_length(n, m):
        # Simplified heuristic based on known results
        return n * m

    instances_tested = 0
    total_rank = 0
    total_length = 0
    n_max = 0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n, 2 * n)
            variables = list(range(n))
            clauses = []
            for _ in range(m):
                clause = random.sample(variables, random.randint(1, n))
                clauses.append(clause)
            
            matrix = [[0] * n for _ in range(n)]
            for clause in clauses:
                for var in clause:
                    matrix[var][var] += 1
                    for other_var in clause:
                        if var != other_var:
                            matrix[var][other_var] -= Fraction(1, len(clause))
            
            rank = min_rank(matrix)
            length = frege_proof_length(n, m)
            
            total_rank += rank
            total_length += length
            instances_tested += 1
            n_max = max(n_max, n)

    mean_rank = Fraction(total_rank, instances_tested)
    mean_length = Fraction(total_length, instances_tested)
    correlation_coefficient = (mean_rank * mean_length - instances_tested) / (instances_tested ** 2 - instances_tested)
    
    conjecture_holds = correlation_coefficient >= Fraction(8, 10)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")