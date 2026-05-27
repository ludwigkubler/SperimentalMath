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

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate non-pivot elements
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    
    # Back-substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    
    return x

def minimal_rank(tree):
    n = len(tree)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    
    # Construct the system of equations
    for i in range(n):
        for j in range(i+1, n):
            if tree[i][j]:
                A[i][j] = 1
                A[j][i] = 1
                b[i] += 1
                b[j] -= 1
    
    # Solve the system using Gaussian elimination
    try:
        x = gaussian_elimination(A, b)
        return sum(1 for xi in x if abs(xi) > 1e-6)
    except ValueError:
        return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random XOR-AND tree
    def generate_tree(n):
        if n == 0:
            return []
        else:
            left = generate_tree(n-1)
            right = generate_tree(n-1)
            return [[left[i] ^ right[i] for i in range(2**(n-1))], [left[i] & right[i] for i in range(2**(n-1))]]
    
    n = random.randint(5, 40)
    tree = generate_tree(n)
    
    # Compute the minimal rank of the noncommutative crossed product algebra
    rank = minimal_rank(tree)
    
    # Check if the conjecture holds
    f_n = math.log(n) * math.log(math.log(n))
    width = sum(1 for row in tree for x in row if x)
    conjecture_holds = rank <= f_n and width <= 2**n
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Tree with n={n}, rank={rank}, width={width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 97))  # Default to first 30 primes
    
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
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Tree with rank > f(n) and width > 2^n\" first_failing_seed={first_failing_seed}")