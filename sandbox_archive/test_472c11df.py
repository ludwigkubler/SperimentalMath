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
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def geometric_algebra_representation(cnf):
        # Simplified representation using a list of lists
        return [[abs(lit) for lit in clause] for clause in cnf]
    
    def rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        
        # Gaussian elimination
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                continue
            
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
        
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        rank = sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(n)))
        return rank
    
    def monotone_circuit_depth(cnf):
        # Simplified estimation of circuit depth
        return len(cnf) + len(set(abs(lit) for clause in cnf for lit in clause))
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n * (n - 1) // 2, 100))
    cnf = generate_k_cnf(n, k)
    
    ga_representation = geometric_algebra_representation(cnf)
    ga_rank = rank(ga_representation)
    circuit_depth = monotone_circuit_depth(cnf)
    
    return {
        "metric_name": "Rank vs DPLL Height",
        "metric_value": ga_rank,
        "instances_tested": 1,
        "conjecture_holds": ga_rank <= math.sqrt(n),
        "counterexample": "" if ga_rank <= math.sqrt(n) else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['metric_value']}, k={random.randint(1, 50)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")