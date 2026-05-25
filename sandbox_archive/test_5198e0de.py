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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find the pivot
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below the pivot
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        # Back substitution
        solution = [0] * n
        for i in range(n-1, -1, -1):
            solution[i] = matrix[i][-1] / matrix[i][i]
            for j in range(i-1, -1, -1):
                matrix[j][-1] -= matrix[j][i] * solution[i]
        
        return solution
    
    def rank(matrix):
        n = len(matrix)
        rref_matrix = [row[:] for row in matrix]
        gaussian_elimination(rref_matrix)
        rank = 0
        for row in rref_matrix:
            if any(row):
                rank += 1
        return rank
    
    def tseitin_formula(n):
        variables = list(range(1, n+1))
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
        for i in range(1, n):
            for j in range(i+1, n+1):
                clauses.append([-i, -j, i+j])
        return variables, clauses
    
    def resolution(clauses):
        new_clauses = set(clauses)
        while True:
            new_clause = None
            for clause1 in new_clauses:
                for clause2 in new_clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [x for x in clause1 + clause2 if x not in set(clause1) & set(clause2)]
                        break
                if new_clause:
                    break
            if new_clause is None:
                return len(new_clauses)
            new_clauses.add(tuple(sorted(new_clause)))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        refutation_length = resolution(clauses)
        q_log_rank = rank([[random.randint(0, 1) for _ in range(n)] for _ in range(n)])
        results.append({
            "n": n,
            "refutation_length": refutation_length,
            "q_log_rank": q_log_rank
        })
    
    total_q_log_rank = sum(result["q_log_rank"] for result in results)
    mean_q_log_rank = total_q_log_rank / len(results)
    std_q_log_rank = math.sqrt(sum((result["q_log_rank"] - mean_q_log_rank) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(result["q_log_rank"] >= 2**(n/4) for n, _, _ in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Quantum Logarithm Rank",
        "metric_value": mean_q_log_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_q_log_rank = sum(result["metric_value"] for result in results)
    mean_q_log_rank = total_q_log_rank / len(results)
    std_q_log_rank = math.sqrt(sum((result["metric_value"] - mean_q_log_rank) ** 2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_q_log_rank} std={std_q_log_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")