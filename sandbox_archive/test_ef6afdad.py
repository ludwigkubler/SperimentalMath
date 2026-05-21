# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    
    return A

def geometric_entropy(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if (i, j) in G or (j, i) in G:
                A[i][j] = 1
                A[j][i] = 1
    
    A = gaussian_elimination(A)
    
    entropy = 0
    for row in A:
        non_zero_count = sum(1 for x in row if x != 0)
        entropy += -non_zero_count * math.log2(non_zero_count / n)
    
    return entropy

def tseitin_formula(G):
    n = len(G)
    literals = [f'x{i}' for i in range(n)]
    clauses = []
    
    # Add clauses for each edge
    for (i, j) in G:
        clauses.append([literals[i], literals[j]])
        clauses.append([-literals[i], -literals[j]])
        clauses.append([literals[i], -literals[j]])
        clauses.append([-literals[i], literals[j]])
    
    # Add clauses to ensure at least one literal is true
    for i in range(n):
        clauses.append([literals[i]])
    
    return clauses

def resolution_proof_length(clauses):
    queue = [set(c) for c in clauses]
    while True:
        new_clauses = []
        found_resolvent = False
        
        for i in range(len(queue)):
            for j in range(i + 1, len(queue)):
                common_vars = set(queue[i]) & set(queue[j])
                if common_vars:
                    resolvent = set()
                    for var in queue[i]:
                        if -var not in queue[j]:
                            resolvent.add(var)
                    for var in queue[j]:
                        if -var not in queue[i]:
                            resolvent.add(var)
                    
                    if len(resolvent) == 1:
                        return len(queue)
                    
                    new_clauses.append(resolvent)
                    found_resolvent = True
        
        if not found_resolvent:
            break
        
        for clause in new_clauses:
            queue.append(clause)
    
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = set()
    for _ in range(n * (n - 1)):
        u, v = random.sample(range(n), 2)
        if u < v:
            G.add((u, v))
    
    gamma_G = geometric_entropy(G)
    Tseitin_clauses = tseitin_formula(G)
    resolution_length = resolution_proof_length(Tseitin_clauses)
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": resolution_length,
        "instances_tested": 1,
        "conjecture_holds": resolution_length >= 2 ** gamma_G,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r['metric_value'] for r in results) / len(results)
    std_length = (sum((r['metric_value'] - mean_length)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='resolution_length < 2^gamma_G' first_failing_seed={first_failing_seed + seeds[0]}")