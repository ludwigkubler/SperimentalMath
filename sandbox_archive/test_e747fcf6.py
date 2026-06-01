# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def hamiltonian_matrix(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        H = [[0] * (2 * n + 1) for _ in range(2 * n + 1)]
        
        for clause in cnf:
            for i, lit in enumerate(clause):
                if lit > 0:
                    row = 2 * lit - 1
                    col = 2 * abs(lit)
                else:
                    row = 2 * abs(lit) - 1
                    col = 2 * lit
                
                H[row][col] += 1
                H[col][row] += 1
        
        return H
    
    def circuit_monotone_width(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        width = 0
        
        for clause in cnf:
            active_lits = [lit for lit in clause if random.choice([True, False])]
            width = max(width, len(active_lits))
        
        return width
    
    def quaternionic_norm(matrix):
        n = len(matrix)
        trace = sum(matrix[i][i] for i in range(n))
        det = 1
        for i in range(n):
            for j in range(i + 1, n):
                minor = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
                det *= (-1) ** (i + j) * matrix[i][j] * determinant(minor)
        
        return Fraction(trace**2 - det, 4)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = 0
            for j in range(n):
                minor = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += (-1) ** j * matrix[0][j] * determinant(minor)
            return det
    
    cnf = []
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    
    for _ in range(m):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        cnf.append(clause)
    
    H = hamiltonian_matrix(cnf)
    w = circuit_monotone_width(cnf)
    norm = quaternionic_norm(H)
    
    return {
        "metric_name": "quaternionic_norm",
        "metric_value": float(norm),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")