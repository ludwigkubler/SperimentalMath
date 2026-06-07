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
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(c) != abs(d) for c, d in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(1, matrix[i][i])
            for j in range(n):
                matrix[i][j] *= factor
            for j in range(n):
                if i != j:
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(abs(x) < 1e-9 for x in matrix[i]):
                continue
            rank += 1
            for j in range(n):
                if i != j:
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def communication_complexity_rank_variance(clauses, n):
        m = len(clauses)
        A = [[0] * (m + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(i+1, m):
                if any(abs(c) == abs(d) for c, d in zip(clauses[i], clauses[j])):
                    A[i][j] = A[j][i] = 1
        A[m][m] = 1
        A = gaussian_elimination(A)
        return rank(A)
    
    def minimal_root_system_length(n):
        # Placeholder function for the actual calculation
        # This is a dummy implementation and should be replaced with the actual formula
        return n
    
    instances_tested = 0
    total_L = 0
    total_w = 0
    max_n = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > max_n:
            max_n = n
        
        for _ in range(5):
            cnf = generate_cnf(n)
            L = minimal_root_system_length(n)
            w = communication_complexity_rank_variance(cnf, n)
            
            total_L += L
            total_w += w
            instances_tested += 1
    
    mean_L = total_L / instances_tested
    mean_w = total_w / instances_tested
    correlation_coefficient = (instances_tested * sum(L * w for L, w in zip([mean_L] * instances_tested, [mean_w] * instances_tested)) - 
                              instances_tested * mean_L * mean_w) / math.sqrt((instances_tested * sum(L**2 for L in [mean_L] * instances_tested) - instances_tested * mean_L**2) *
                                                                 (instances_tested * sum(w**2 for w in [mean_w] * instances_tested) - instances_tested * mean_w**2))
    
    conjecture_holds = 0.8 <= correlation_coefficient <= 1
    counterexample = "" if conjecture_holds else "correlation_outside_range"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")