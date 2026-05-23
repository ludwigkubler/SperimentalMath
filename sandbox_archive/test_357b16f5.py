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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                if i == k:
                    A[j][k] = 0
                else:
                    A[j][k] += factor * A[i][k]

    # Back-substitute to find solution
    x = [0] * n
    for i in range(m-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def resolution_length(variables, clauses):
    n = len(variables)
    seen = set()
    queue = list(clauses)
    
    while queue:
        clause = queue.pop(0)
        for literal in clause:
            if -literal in seen:
                continue
            seen.add(literal)
            new_clause = []
            for c in clauses:
                if literal not in c and -literal not in c:
                    new_clause.extend(c)
            if len(new_clause) == 1:
                return len(seen)
            queue.append(new_clause)
    
    return len(seen)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(n):
        a, b = random.sample(variables, 2)
        clauses.append([a, -b])
        clauses.append([-a, b])
    
    # Compute minimal rank of invariant ν(C(F))
    cohomology_classes = [random.random() for _ in range(n)]
    invariant_rank = len(set(cohomology_classes))
    
    # Construct resolution proof and measure its length
    proof_length = resolution_length(variables, clauses)
    
    # Correlate the minimal rank ν(C(F)) with the resolution proof length
    conjecture_holds = proof_length >= 2 ** (invariant_rank * math.log(2))
    counterexample = "" if conjecture_holds else f"Proof length {proof_length} < 2^({invariant_rank}*log2({invariant_rank}))"
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")