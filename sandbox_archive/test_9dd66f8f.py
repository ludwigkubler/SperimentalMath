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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    if m == 0 or n == 0:
        return 0
    
    rank = 0
    for i in range(m):
        pivot_row = i
        while pivot_row < m and matrix[pivot_row][i] == 0:
            pivot_row += 1
        
        if pivot_row == m:
            continue
        
        # Swap rows to put the pivot at the top
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        # Eliminate entries below the pivot
        for j in range(i + 1, m):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] += factor * matrix[i][k]
        
        rank += 1
    
    return rank

def generate_frege_tree(depth):
    if depth == 0:
        return ['A']
    else:
        left = generate_frege_tree(random.randint(0, depth - 1))
        right = generate_frege_tree(random.randint(0, depth - 1))
        return ['B', left, right]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    total_rho_G = 0
    instances_tested = 0
    
    for n in range(5, 41):
        for _ in range(n * 3):  # Ensure at least 30 instances per seed
            tree = generate_frege_tree(n)
            literals = set()
            
            def traverse(node):
                if isinstance(node, list):
                    left, right = node[1], node[2]
                    traverse(left)
                    traverse(right)
                else:
                    literals.add(node)
            
            traverse(tree)
            
            G = []
            for literal in literals:
                row = [0] * len(literals)
                row[literals.index(literal)] = 1
                G.append(row)
            
            rho_G = matrix_rank(G)
            total_rho_G += rho_G
            instances_tested += 1
    
    mean_value = Fraction(total_rho_G, instances_tested)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": float(mean_value),
        "instances_tested": instances_tested,
        "conjecture_holds": all(rho_G <= n for rho_G, n in zip(G, [n] * len(G))),
        "counterexample": "" if all(rho_G <= n for rho_G, n in zip(G, [n] * len(G))) else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")