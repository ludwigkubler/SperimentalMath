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

def generate_cnf(n):
    cnf = []
    for _ in range(10 * n):  # Generate enough clauses to ensure variety
        clause = set()
        while len(clause) < 2:
            lit = random.randint(-n, -1)
            if lit not in clause and -lit not in clause:
                clause.add(lit)
        cnf.append(list(clause))
    return cnf

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        if any(matrix[j][i] != 0 for j in range(m)):
            rank += 1
            for j in range(m):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            for k in range(n):
                matrix[pivot_row][k], matrix[i][k] = matrix[i][k], matrix[pivot_row][k]
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        matrix = [[0] * (n + 1) for _ in range(n)]
        
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    matrix[lit - 1][lit] += 1
                else:
                    matrix[-lit - 1][-lit] += 1
        
        rank = matrix_rank(matrix)
        resolution_width = len(cnf) + n  # Simplified heuristic for resolution width
        
        results.append({
            "n": n,
            "rank": rank,
            "resolution_width": resolution_width
        })
    
    if not results:
        return {
            "metric_name": "Ratio of Rank to Resolution Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    total_rank = sum(result["rank"] for result in results)
    total_width = sum(result["resolution_width"] for result in results)
    mean_ratio = Fraction(total_rank, total_width).limit_denominator()
    
    return {
        "metric_name": "Ratio of Rank to Resolution Width",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": mean_ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [3, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    ratios = [result["metric_value"] for result in results if result["instances_tested"] > 0]
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(r is not None and r <= 2 for r in ratios):
        print(f"RESULT: SUPPORTED mean={sum(ratios)/len(ratios)} std=NA support_fraction={support_fraction}")
    elif any(r > 2 for r in ratios):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 2)
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds 2' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")