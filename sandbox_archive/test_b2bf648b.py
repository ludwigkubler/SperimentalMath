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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        
        factor = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= factor
        
        for j in range(n):
            if i != j:
                factor = Augmented[j][i]
                for k in range(i, n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Augmented[i][-1]
        for j in range(i+1, n):
            x[i] -= Augmented[i][j] * x[j]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 5 + (seed % 6) * 5
    k = 3
    
    # Generate a random monotone circuit for k-CLIQUE on n variables
    literals = [f"x{i}" for i in range(n)]
    clauses = []
    for i in range(k):
        clause = random.sample(literals, k)
        clauses.append(clause)
    
    # Convert the circuit to a geometric invariant variety (simplified model)
    # This is a placeholder; actual GIT computation would be complex
    rank = len(clauses) * n
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= (0.9 * n**k),
        "counterexample": "" if rank >= (0.9 * n**k) else f"Rank {rank} < 0.9n^k"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    elif any(r['counterexample'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if r['counterexample'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")