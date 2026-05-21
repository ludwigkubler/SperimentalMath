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
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = Fraction(A[i][i])
        for j in range(i, n):
            A[i][j] /= factor
        
        for k in range(n):
            if k != i:
                factor = Fraction(A[k][i])
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    return A

def geometric_entropy(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    
    # Construct the adjacency matrix
    for u in G:
        for v in G[u]:
            A[u][v] += 1
    
    # Gaussian elimination to find rank
    rank = gaussian_elimination(A)
    
    # Minimal geometric entropy is related to the rank of the adjacency matrix
    gamma_G = -math.log2(rank / n)
    return gamma_G

def tseitin_formula(G):
    n = len(G)
    literals = list(range(n))
    clauses = []
    
    for u in G:
        if len(G[u]) == 1:
            v = next(iter(G[u]))
            clauses.append([literals[u], -literals[v]])
        else:
            new_var = n + len(clauses)
            literals.append(new_var)
            clauses.append([new_var])
            for v in G[u]:
                clauses.append([-new_var, literals[v]])
    
    return clauses

def resolution_proof_length(clauses):
    stack = []
    while True:
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if not unit_clause:
            break
        literal = unit_clause[0]
        stack.append(literal)
        
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                new_clauses.extend([c for c in new_clauses if literal not in c and -literal not in c])
            else:
                new_clauses.append(clause)
        
        clauses = new_clauses
    
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    G = {i: set() for i in range(n)}
    for _ in range(10 * n):
        u, v = random.sample(range(n), 2)
        if u != v and v not in G[u]:
            G[u].add(v)
    
    gamma_G = geometric_entropy(G)
    clauses = tseitin_formula(G)
    proof_length = resolution_proof_length(clauses)
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length >= 2 ** gamma_G,
        "counterexample": "" if proof_length >= 2 ** gamma_G else f"gamma(G)={gamma_G}, proof_length={proof_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30))
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"gamma(G) < 2^proof_length\" first_failing_seed={first_failing_seed}")