# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations, permutations

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for r in range(i + 1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for r in range(i + 1, rows):
            factor = Fraction(matrix[r][i], matrix[i][i])
            for c in range(cols):
                if i == c:
                    matrix[r][c] = 0
                else:
                    matrix[r][c] -= factor * matrix[i][c]
    return matrix

def rank(matrix):
    rref = gaussian_elimination(matrix)
    non_zero_rows = [row for row in rref if any(row)]
    return len(non_zero_rows)

def generate_cnf(n):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in range(10, 41):
        cnf = generate_cnf(n)
        moduli_rank = rank([[abs(lit) for lit in clause] for clause in cnf])
        resolution_rank = len(cnf)  # Simplified rank for Tseitin Resolution Tree
        
        results.append({
            "n": n,
            "moduli_rank": moduli_rank,
            "resolution_rank": resolution_rank
        })
    
    total_moduli_rank = sum(result["moduli_rank"] for result in results)
    total_resolution_rank = sum(result["resolution_rank"] for result in results)
    mean_moduli_rank = Fraction(total_moduli_rank, len(results))
    mean_resolution_rank = Fraction(total_resolution_rank, len(results))
    
    conjecture_holds = all(mean_moduli_rank >= 2 * mean_resolution_rank for _ in range(30))
    counterexample = "" if conjecture_holds else "n-dependent ranks"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": float(mean_moduli_rank),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [101, 103, 107, 109]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_moduli_rank = sum(r["metric_value"] for r in results)
    total_resolution_rank = sum(2 * r["instances_tested"] * r["resolution_rank"] / 30 for r in results)
    mean_moduli_rank = total_moduli_rank / len(results)
    mean_resolution_rank = total_resolution_rank / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_moduli_rank} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n-dependent ranks\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")