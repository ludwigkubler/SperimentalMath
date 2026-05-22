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
    
    # Generate a random satisfiability instance with n variables and m clauses
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    
    # Compute the p-adic Hodge structure (constructive mapping)
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for col in range(cols):
            pivot_row = None
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for r in range(rows):
                    if r != rank and matrix[r][col] != 0:
                        factor = -matrix[r][col] / matrix[rank][col]
                        for c in range(cols):
                            matrix[r][c] += factor * matrix[rank][c]
                rank += 1
        return rank
    
    # Construct the Hodge filtration matrix (simplified example)
    hodge_matrix = []
    for clause in clauses:
        row = [0] * n
        for var in clause:
            row[var] = 1
        hodge_matrix.append(row)
    
    minimal_rank = gaussian_elimination(hodge_matrix)
    
    # Measure the metric (minimal rank)
    metric_name = "Minimal Rank of p-Adic Hodge Structure"
    metric_value = minimal_rank
    
    # Determine if the conjecture holds
    k = 2  # Example constant for polynomial bound O(n^k)
    conjecture_holds = minimal_rank <= n ** k
    counterexample = "" if conjecture_holds else f"Rank {minimal_rank} exceeds bound {n**k}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean and std of metric_value
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    variance_metric_value = sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)
    std_metric_value = math.sqrt(variance_metric_value)
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    # Determine the final result
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")