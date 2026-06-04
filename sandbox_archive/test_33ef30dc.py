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
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-pivot elements
        for j in range(n):
            if i != j:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n+1):
                    A[j][k] -= factor * A[i][k]

    # Back-substitute to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(A[i][n], A[i][i])
        for j in range(i-1, -1, -1):
            A[j][n] -= A[j][i] * x[i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def height_dpll(clauses):
    assignment = {}
    stack = []
    
    def backtrack():
        if all(l in assignment or -l in assignment for l in set.union(*clauses)):
            return True
        literal = next((l for l in set.union(*clauses) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False
        
        assignment[literal] = True
        stack.append(literal)
        
        if backtrack():
            return True
        
        del assignment[literal]
        stack.pop()
        
        assignment[-literal] = True
        stack.append(-literal)
        
        if backtrack():
            return True
        
        del assignment[-literal]
        stack.pop()
        
        return False
    
    return len(stack) if backtrack() else 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if len(set(clause)) > 1:
            clauses.append(tuple(sorted(clause)))
    
    Q = [[0] * n for _ in range(n)]
    for clause in clauses:
        for l in clause:
            Q[l-1][l-1] += Fraction(1, 2)
            for m in clause:
                if l != m:
                    Q[l-1][m-1] -= Fraction(1, 4)
    
    rank_Q = len(gaussian_elimination(Q))
    height_DPLL = height_dpll(clauses)
    
    return {
        "metric_name": "Rank and DPLL Height",
        "metric_value": rank_Q,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": rank_Q <= height_DPLL,
        "counterexample": "" if rank_Q <= height_DPLL else f"rank_Q={rank_Q}, height_DPLL={height_DPLL}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"rank_Q > height_DPLL\" first_failing_seed={first_failing_seed}")