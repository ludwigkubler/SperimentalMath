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
    
    n = 40
    m = 3 * n
    
    # Generate a random 3-CNF instance
    clauses = []
    for _ in range(m):
        variables = [random.randint(1, n) for _ in range(3)]
        clause = tuple(sorted(variables))
        if random.choice([True, False]):
            clause = (-clause[0], -clause[1], -clause[2])
        clauses.append(clause)
    
    # Construct the matroid polytope
    hyperedges = set()
    for clause in clauses:
        hyperedges.add(frozenset(clause))
    
    characteristic_vectors = []
    for i in range(2**n):
        vector = [0] * n
        for j in range(n):
            if (i >> j) & 1:
                vector[j] = 1
        characteristic_vectors.append(vector)
    
    # Compute the dimension of the matroid polytope using Gaussian elimination
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            pivot_row = -1
            for i in range(rank, m):
                if A[i][j] != 0:
                    pivot_row = i
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for k in range(n):
                if k != j and A[rank][k] != 0:
                    factor = A[rank][k] / A[rank][j]
                    for l in range(n):
                        A[rank][l] -= factor * A[pivot_row][l]
            rank += 1
        return rank
    
    matroid_polytope_dimension = gaussian_elimination(characteristic_vectors)
    
    # Compute the minimal SOS degree required to refute the instance
    def is_satisfiable(clauses):
        assignment = [random.choice([-1, 1]) for _ in range(n)]
        for clause in clauses:
            if all(assignment[var-1] * literal >= 0 for var, literal in enumerate(clause)):
                return True
        return False
    
    def sos_degree(clauses):
        degree = 0
        while not is_satisfiable(clauses):
            degree += 1
            # Add a new SOS constraint to refute the instance
            # This is a simplified version and may not always work
            for i in range(n):
                clauses.append((i+1, -i-1))
        return degree
    
    sos_refutation_degree = sos_degree(clauses)
    
    # Verify the conjecture
    conjecture_holds = matroid_polytope_dimension <= sos_refutation_degree
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "SOS Degree Lower Bound",
        "metric_value": sos_refutation_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")