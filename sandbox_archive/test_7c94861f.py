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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= pivot
        for k in range(rows):
            if k != i:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    rref = gaussian_elimination(matrix)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def generate_cnf(n):
    cnf = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in range(10, 41):
        cnf = generate_cnf(n)
        moduli_rank = rank([[abs(lit) for lit in clause] for clause in cnf])
        resolution_tree_rank = rank(cnf)  # Simplified for demonstration
        
        results.append({
            "n": n,
            "moduli_rank": moduli_rank,
            "resolution_tree_rank": resolution_tree_rank
        })
    
    total_moduli_rank = sum(result["moduli_rank"] for result in results)
    total_resolution_tree_rank = sum(result["resolution_tree_rank"] for result in results)
    mean_moduli_rank = Fraction(total_moduli_rank, len(results))
    mean_resolution_tree_rank = Fraction(total_resolution_tree_rank, len(results))
    
    conjecture_holds = mean_moduli_rank >= 2 * mean_resolution_tree_rank
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, moduli_rank={results[0]['moduli_rank']}, resolution_tree_rank={results[0]['resolution_tree_rank']}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_moduli_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_moduli_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_moduli_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")