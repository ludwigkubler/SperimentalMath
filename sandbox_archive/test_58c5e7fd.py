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

# Helper functions for matrix operations
def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    
    for i in range(n):
        # Find the pivot row
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, m):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    # Back-substitute to find the solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i+1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
        x[i] /= augmented_matrix[i][i]
    
    return x

def determinant(A):
    m = len(A)
    if m == 1:
        return A[0][0]
    det = Fraction(0)
    for j in range(m):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

def monodromy_group_order(f):
    n = len(f)
    if n == 1:
        return 2
    
    # Generate all possible assignments
    assignments = [list(range(2)) for _ in range(n)]
    all_assignments = list(itertools.product(*assignments))
    
    # Find the monodromy group elements
    monodromy_elements = set()
    for perm in itertools.permutations(range(n)):
        new_f = []
        for assignment in all_assignments:
            new_assignment = [assignment[perm[i]] for i in range(n)]
            new_f.append(new_assignment)
        if new_f == f:
            monodromy_elements.add(tuple(perm))
    
    # The order of the monodromy group is the number of unique permutations
    return len(monodromy_elements)

def communication_complexity_rank(f):
    n = len(f)
    if n == 1:
        return 1
    
    # Generate all possible assignments
    assignments = [list(range(2)) for _ in range(n)]
    all_assignments = list(itertools.product(*assignments))
    
    # Find the rank of the communication complexity matrix
    M = []
    for assignment in all_assignments:
        row = []
        for i in range(n):
            row.append(assignment[i])
        M.append(row)
    
    det = determinant(M)
    if det == 0:
        return n
    
    return n - 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    c = Fraction(1, 2)  # Example constant for the bound
    
    results = []
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        f = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
        
        order = monodromy_group_order(f)
        rank = communication_complex_rank(f)
        
        lower_bound = c * n**c * math.log(n)
        upper_bound = c * n**c * math.log(n)
        
        results.append({
            "order": order,
            "rank": rank,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound
        })
    
    total_order = sum(result["order"] for result in results)
    total_rank = sum(result["rank"] for result in results)
    mean_order = total_order / instances_tested
    mean_rank = total_rank / instances_tested
    
    conjecture_holds = all(
        result["order"] >= result["lower_bound"] and result["rank"] <= result["upper_bound"]
        for result in results
    )
    
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "monodromy_group_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")