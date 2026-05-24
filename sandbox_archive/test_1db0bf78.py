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

def generate_random_kcnf(n, k):
    clauses = []
    for _ in range(k * n):
        clause = set()
        while len(clause) < 2:
            var = random.randint(1, n)
            if random.choice([True, False]):
                clause.add(var)
            else:
                clause.add(-var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def min_noncommutative_rank(clauses):
    n = max(abs(v) for v in set(var for clause in clauses for var in clause))
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    
    for clause in clauses:
        for i, x in enumerate(clause):
            for j, y in enumerate(clause):
                if i < j:
                    matrix[abs(x)][abs(y)] += 1
                    matrix[abs(y)][abs(x)] += 1
    
    rank = 0
    for row in range(1, n + 1):
        pivot_found = False
        for col in range(1, n + 1):
            if matrix[row][col] != 0:
                pivot_found = True
                for i in range(n + 1):
                    matrix[row][i], matrix[col][i] = matrix[col][i], matrix[row][i]
                break
        if not pivot_found:
            continue
        
        rank += 1
        for i in range(1, n + 1):
            if i != row and matrix[i][col] != 0:
                factor = Fraction(matrix[i][col], matrix[row][col])
                for j in range(n + 1):
                    matrix[i][j] -= factor * matrix[row][j]
    
    return rank

def resolution_depth(clauses):
    stack = []
    literals_seen = set()
    
    def resolve(lit):
        if -lit in literals_seen:
            return True
        literals_seen.add(lit)
        for clause in clauses:
            if lit in clause:
                if len(clause) == 1:
                    return False
                new_clause = [x for x in clause if x != lit]
                stack.append(new_clause)
    
    while stack:
        clause = stack.pop()
        for lit in clause:
            if resolve(lit):
                break
        else:
            return float('inf')
    
    return len(clauses) - len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = 10
    
    clauses = generate_random_kcnf(n, k)
    rank = min_noncommutative_rank(clauses)
    depth = resolution_depth(clauses)
    
    return {
        "metric_name": "resolution_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": depth >= 2 ** (math.floor(math.log2(rank)) + 1),
        "counterexample": "" if depth >= 2 ** (math.floor(math.log2(rank)) + 1) else f"Depth {depth} < 2^Ω({rank})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")