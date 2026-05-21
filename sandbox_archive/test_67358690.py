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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0]) if matrix else 0
    for i in range(rows):
        # Find a pivot row
        pivot_row = i
        while pivot_row < rows and matrix[pivot_row][i] == 0:
            pivot_row += 1
        if pivot_row == rows:
            continue
        
        # Swap the current row with the pivot row
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        # Eliminate entries below the pivot
        for j in range(i + 1, rows):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] += factor * matrix[i][k]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = random.randint(5, 30)
    k = 10
    
    # Generate a random 3-CNF formula
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(2, 3))]
        clauses.append(clause)
    
    # Convert to monotone DNF using resolution
    dnf_clauses = []
    while len(clauses) > 0:
        new_clause = None
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                if any(abs(x) == abs(y) and (x != y) for x in clauses[i] for y in clauses[j]):
                    new_clause = [x for x in clauses[i] if x not in clauses[j]]
                    break
            if new_clause:
                break
        if new_clause is None:
            dnf_clauses.extend(clauses)
            break
        clauses.remove(new_clause)
    
    # Construct the binary matrix
    matrix = []
    for clause in dnf_clauses:
        row = [0] * n
        for var in clause:
            row[abs(var) - 1] = 1 if var > 0 else -1
        matrix.append(row)
    
    # Compute the rank of the matroid
    rank = gaussian_elimination(matrix)
    
    # Determine if the conjecture holds
    if m <= n ** 2:
        conjecture_holds = rank >= 0.8 * n
    elif m >= n ** (k ** 0.25):
        conjecture_holds = rank <= 5 * math.log(n)
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": len(dnf_clauses),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank} does not meet the expected bound for m={m}, n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank does not meet the expected bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")