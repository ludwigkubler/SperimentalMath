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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses
    
    def cnf_to_symmetric_matrix(cnf):
        n = max(abs(x) for x in set(y for clause in cnf for y in clause))
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i in clause:
                for j in clause:
                    if i != j:
                        matrix[abs(i)][abs(j)] += 1
        return matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for r in range(i+1, n):
                if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                    max_row = r
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            for r in range(i+1, n):
                factor = Fraction(matrix[r][i], matrix[i][i])
                for c in range(i, n + 1):
                    matrix[r][c] -= factor * matrix[i][c]
        
        return matrix
    
    def min_index_of_quotients(matrix):
        n = len(matrix)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        quotient_matrix = []
        for i in range(n):
            row = [matrix[i][j] - identity[i][j] for j in range(n)]
            quotient_row = [sum(row[j] * matrix[j][k] for k in range(n)) for j in range(n)]
            quotient_matrix.append(quotient_row)
        
        reduced_quotient_matrix = gaussian_elimination(quotient_matrix)
        min_index = 1
        for row in reduced_quotient_matrix:
            min_index *= sum(x != 0 for x in row)
        return min_index
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        p = next((x for x in range(1, len(cnf) + 1) if x not in assignment and -x not in assignment), None)
        if p is None:
            return False
        
        assignment[p] = True
        if dpll([c for c in cnf if all(abs(x) != p for x in c)], assignment):
            return True
        del assignment[p]
        
        assignment[-p] = True
        if dpll([c for c in cnf if all(abs(x) != -p for x in c)], assignment):
            return True
        del assignment[-p]
        
        return False
    
    def dpll_proof_depth(cnf):
        assignment = {}
        depth = 0
        
        def backtrack():
            nonlocal depth
            p = next((x for x in range(1, len(cnf) + 1) if x not in assignment and -x not in assignment), None)
            if p is None:
                return True
            
            assignment[p] = True
            depth += 1
            if backtrack():
                return True
            del assignment[p]
            depth -= 1
            
            assignment[-p] = True
            depth += 1
            if backtrack():
                return True
            del assignment[-p]
            depth -= 1
            
            return False
        
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, int(n * (n - 1) / 2)))
            matrix = cnf_to_symmetric_matrix(cnf)
            min_index = min_index_of_quotients(matrix)
            proof_depth = dpll_proof_depth(cnf)
            
            if min_index == 0 or proof_depth == 0:
                continue
            
            results.append({
                "n": n,
                "min_index": min_index,
                "proof_depth": proof_depth
            })
    
    if not results:
        return {
            "metric_name": "log_min_index",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    log_min_indices = [math.log(result["min_index"]) for result in results]
    proof_depths = [result["proof_depth"] for result in results]
    
    mean_log_min_index = sum(log_min_indices) / len(log_min_indices)
    mean_proof_depth = sum(proof_depths) / len(proof_depths)
    
    correlation_coefficient = 0
    if len(log_min_indices) > 1:
        numerator = sum((log_min_indices[i] - mean_log_min_index) * (proof_depths[i] - mean_proof_depth) for i in range(len(log_min_indices)))
        denominator = math.sqrt(sum((x - mean_log_min_index) ** 2 for x in log_min_indices)) * math.sqrt(sum((y - mean_proof_depth) ** 2 for y in proof_depths))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "log_min_index",
        "metric_value": mean_log_min_index,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": "" if abs(correlation_coefficient) >= 0.7 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")