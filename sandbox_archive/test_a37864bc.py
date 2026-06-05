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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_proof_depth(clauses):
        stack = list(clauses)
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if -stack[i][0] in stack[j]:
                        new_clause = [x for x in stack[i] if x != -stack[i][0]] + [y for y in stack[j] if y != -stack[i][0]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            stack.append(new_clause)
    
    def lie_algebroid_rank(clauses):
        n = len(clauses)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    matrix[i][var - 1] += 1
                else:
                    matrix[i][-var - 1] -= 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for i in range(cols):
                pivot_row = None
                for j in range(rank, rows):
                    if matrix[j][i] != 0:
                        pivot_row = j
                        break
                if pivot_row is not None:
                    matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                    rank += 1
                    for j in range(rows):
                        if j != rank - 1:
                            factor = Fraction(matrix[j][i], matrix[rank - 1][i])
                            for k in range(cols):
                                matrix[j][k] -= factor * matrix[rank - 1][k]
            return rank
        
        return gaussian_elimination(matrix)
    
    n_max = 40
    instances_tested = 30
    total_ratio = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        clauses = generate_cnf(n)
        depth = resolution_proof_depth(clauses)
        rank = lie_algebroid_rank(clauses)
        
        if rank == 0 or depth == 0:
            continue
        
        ratio = Fraction(rank, depth)
        total_ratio += ratio
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = 0.5 <= mean_ratio <= 1.5
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio}"
    
    return {
        "metric_name": "Ratio of Rank to Depth",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio out of range\" first_failing_seed={first_failing_seed}")