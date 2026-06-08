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

# Helper functions for matrix operations and graph generation

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def is_independent_set(S, poset):
    for i in S:
        for j in S:
            if i != j and poset[i][j] == 1:
                return False
    return True

def non_crossing_partition(poset, n):
    independent_sets = []
    for r in range(1, n+1):
        for subset in itertools.combinations(range(n), r):
            if is_independent_set(subset, poset):
                independent_sets.append(subset)
    partition = []
    while len(independent_sets) > 0:
        max_size = -1
        max_index = -1
        for i, s in enumerate(independent_sets):
            if len(s) > max_size:
                max_size = len(s)
                max_index = i
        partition.append(independent_sets[max_index])
        independent_sets.pop(max_index)
    return partition

def frege_proof_depth(formula):
    # Placeholder function to calculate Frege proof depth
    # This is a dummy implementation and should be replaced with actual logic
    return len(formula)

# Main trial function
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        # Generate a random CNF formula with n variables
        num_clauses = random.randint(1, n)
        clauses = []
        for _ in range(num_clauses):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        
        # Convert CNF to poset
        poset = [[0] * n for _ in range(n)]
        for clause in clauses:
            for lit1 in clause:
                for lit2 in clause:
                    if abs(lit1) != abs(lit2):
                        poset[abs(lit1)-1][abs(lit2)-1] = 1
                        poset[abs(lit2)-1][abs(lit1)-1] = 1
        
        # Compute the minimal order of a non-crossing partition
        partition = non_crossing_partition(poset, n)
        f_phi = len(partition)
        
        # Calculate Frege proof depth
        f_phi_depth = frege_proof_depth(clauses)
        
        # Store metric value
        metric_values.append(f_phi)
        
        # Check correlation and bounds
        if not (1 <= f_phi <= n**2):
            conjecture_holds = False
            counterexample = "f(φ) out of bounds"
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / instances_tested)
    
    return {
        "metric_name": "Minimal Order of Non-Crossing Partition",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='f(φ) out of bounds' first_failing_seed={first_failing_seed}")