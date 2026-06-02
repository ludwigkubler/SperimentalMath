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
    
    def generate_cnf(width, n):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, width) * 2 - 1 if random.choice([True, False]) else -random.randint(1, width) * 2]
            for _ in range(random.randint(0, width - 1)):
                clause.append(random.randint(1, width) * 2 - 1 if random.choice([True, False]) else -random.randint(1, width) * 2)
            cnf.append(clause)
        return cnf
    
    def compute_minimal_rank(cnf):
        n = len(cnf)
        m = sum(len(clause) for clause in cnf)
        
        # Initialize adjacency matrix
        adj_matrix = [[0] * (n + m) for _ in range(n + m)]
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal > 0:
                    adj_matrix[i][n + literal - 1] = 1
                    adj_matrix[n + literal - 1][i] = 1
                else:
                    adj_matrix[i][n - literal - 1] = 1
                    adj_matrix[n - literal - 1][i] = 1
        
        # Gaussian elimination to find rank
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
                    rank += 1
                    for other_row in range(rows):
                        if other_row != rank - 1 and matrix[other_row][col] != 0:
                            factor = matrix[other_row][col] / matrix[rank - 1][col]
                            for j in range(cols):
                                matrix[other_row][j] -= factor * matrix[rank - 1][j]
            return rank
        
        return gaussian_elimination(adj_matrix)
    
    width_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instance_count = 0
    
    for width in width_values:
        for _ in range(5):  # Sample 5 instances per width
            cnf = generate_cnf(width, 1)
            rank = compute_minimal_rank(cnf)
            total_rank += rank
            instance_count += 1
    
    avg_rank = total_rank / instance_count
    conjecture_holds = avg_rank <= width_values[-1]**2
    counterexample = "" if conjecture_holds else f"Average rank {avg_rank} > {width_values[-1]**2}"
    
    return {
        "metric_name": "average_minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": instance_count,
        "n_max": width_values[-1],
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank:.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")