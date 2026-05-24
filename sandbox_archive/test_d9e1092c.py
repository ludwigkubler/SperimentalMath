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
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        factor = Fraction(1, A[i][i])
        for j in range(i+1, n):
            A[j][i] *= factor
        
        # Eliminate above pivot
        for j in range(i):
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return sum(1 for row in A if any(row))

def rank(Q):
    n = len(Q)
    A = [[Fraction(Q[i][j]) for j in range(n)] for i in range(n)]
    return gaussian_elimination(A)

def tseitin_formula(G, n):
    clauses = []
    for v in range(n):
        clauses.append([v + 1])
        for u in G[v]:
            clauses.append([-u - 1, v + 1])
            clauses.append([-v - 1, u + 1])
    return clauses

def resolution_length(clauses):
    # Simplified version of Resolution algorithm
    queue = set()
    for clause in clauses:
        queue.add(tuple(sorted(clause)))
    
    while True:
        new_clauses = set()
        for c1 in queue:
            for c2 in queue:
                if len(c1) + len(c2) > 30:  # Avoid excessive computation
                    continue
                common = [x for x in c1 if -x in c2]
                if common:
                    new_clause = tuple(sorted(set(c1 + c2) - set(common)))
                    if not new_clause:
                        return len(queue)
                    new_clauses.add(new_clause)
        if new_clauses.issubset(queue):
            break
        queue.update(new_clauses)
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30
    G = []
    for _ in range(n):
        neighbors = set()
        while len(neighbors) < 2:
            neighbor = random.randint(0, n-1)
            if neighbor != _ and neighbor not in neighbors:
                neighbors.add(neighbor)
        G.append(list(neighbors))
    
    Q = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    rank_Q = rank(Q)
    
    clauses = tseitin_formula(G, n)
    proof_length = resolution_length(clauses)
    
    expected_length = 2**(n/8) + 3 * (n**0.5)  # Approximation to o(n)
    diff = abs(proof_length - expected_length)
    
    conjecture_holds = proof_length >= expected_length
    counterexample = "" if conjecture_holds else f"Proof length {proof_length} < {expected_length}"
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"proof_length_too_short\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")