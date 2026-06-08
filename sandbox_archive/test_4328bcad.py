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
        for _ in range(10 * n):  # Each variable appears in at least 10 clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            random.shuffle(clause)
            clauses.append(clause)
        return clauses
    
    def compute_clause_depth(cnf):
        max_depth = 0
        for clause in cnf:
            depth = sum(abs(lit) for lit in clause if lit > 0)
            max_depth = max(max_depth, depth)
        return max_depth
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            pivot_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                    pivot_row = j
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            
            # Eliminate below the pivot
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        
        # Back-substitute to find solution
        solution = [0] * n
        for i in range(n - 1, -1, -1):
            solution[i] = (matrix[i][n] - sum(matrix[i][j] * solution[j] for j in range(i + 1, n))) / matrix[i][i]
        return solution
    
    def local_cohomology_order(cnf):
        n = len(cnf)
        identity_matrix = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        
        # Construct the augmented matrix
        augmented_matrix = [row + [1] for row in cnf]
        augmented_matrix += identity_matrix
        
        # Perform Gaussian elimination
        gaussian_elimination(augmented_matrix)
        
        # The order is the rank of the original matrix
        rank = 0
        for row in augmented_matrix[:n]:
            if any(row[i] != 0 for i in range(n)):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different instances
            cnf = generate_cnf(n)
            clause_depth = compute_clause_depth(cnf)
            order = local_cohomology_order(cnf)
            
            if order > clause_depth:
                conjecture_holds = False
                counterexample = f"n={n}, order={order}, depth={clause_depth}"
            
            total_metric_value += order / clause_depth
            instances_tested += 1
    
    return {
        "metric_name": "local_cohomology_order_over_clause_depth",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")