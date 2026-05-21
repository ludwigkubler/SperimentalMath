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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                clause[random.randint(0, n-1)] = random.choice([-1, 1])
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            if matrix[i][i] == 0:
                continue
            
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def volume_of_hypersurface(cnf):
        n = len(cnf)
        A = [[0] * (n+1) for _ in range(n+1)]
        for i, clause in enumerate(cnf):
            for j in range(n):
                A[i][j] = clause[j]
            A[i][n] = 1
        
        A = gaussian_elimination(A)
        
        volume = 1
        for i in range(n):
            if A[i][i] == 0:
                return float('inf')
            volume *= abs(A[i][i])
        
        return volume
    
    def resolution_proof_length(cnf):
        n = len(cnf)
        clauses = set(tuple(clause) for clause in cnf)
        proof = []
        
        while True:
            new_clauses = set()
            for clause1, clause2 in itertools.combinations(clauses, 2):
                if any(abs(lit1) == abs(lit2) and lit1 != lit2 for lit1 in clause1 for lit2 in clause2):
                    new_clause = tuple(sorted(set(lit for lit in clause1 + clause2 if lit != -lit)))
                    if len(new_clause) == 1:
                        return len(proof)
                    new_clauses.add(new_clause)
            clauses.update(new_clauses)
            proof.append(len(clauses))
        
        return float('inf')
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    min_volume = volume_of_hypersurface(cnf)
    resolution_length = resolution_proof_length(cnf)
    
    if min_volume == float('inf') or resolution_length == float('inf'):
        return {
            "metric_name": "min_volume",
            "metric_value": min_volume,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    conjecture_holds = resolution_length <= 2 ** (min_volume / 2) and min_volume >= 2 ** n
    
    return {
        "metric_name": "min_volume",
        "metric_value": min_volume,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"resolution_length={resolution_length}, expected <= {2 ** (min_volume / 2)}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")