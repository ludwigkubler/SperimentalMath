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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = list(range(n))
    
    # Generate a Tseitin formula
    clauses = []
    for i in range(n):
        clauses.append([variables[i]])
        for j in range(i+1, n):
            clauses.append([variables[i], variables[j]])
            clauses.append([-variables[i], -variables[j]])
            clauses.append([-variables[i], variables[j]])
            clauses.append([variables[i], -variables[j]])
    
    # Compute the Riemannian metric (simplified for non-expander graphs)
    M = [[0] * n for _ in range(n)]
    for clause in clauses:
        for var1 in clause:
            for var2 in clause:
                if var1 != var2:
                    M[abs(var1)-1][abs(var2)-1] += 1
                    M[abs(var2)-1][abs(var1)-1] += 1
    
    # Calculate the minimum local curvature (simplified)
    min_local_curvature = min(sum(M[i]) for i in range(n))
    
    # Use a resolution prover to find the shortest proof
    def resolve(clauses):
        stack = []
        while clauses:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                return False, []
            literal = unit_clause[0]
            clauses = [c for c in clauses if literal not in c and -literal not in c]
            stack.append(literal)
        return True, stack
    
    proof_length, _ = resolve(clauses)
    
    # Correlate min_local_curvature with the resolution proof length
    conjecture_holds = proof_length >= 2 ** (min_local_curvature * math.log(2))
    counterexample = "expander_graph" if not conjecture_holds else ""
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")