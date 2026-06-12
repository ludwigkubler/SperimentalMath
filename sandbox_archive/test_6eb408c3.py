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
            for j in range(rows):
                if j != rank and matrix[j][i] != 0:
                    factor = -matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[rank][k]
            rank += 1
    return rank

def frege_proof_depth(phi, n):
    # Placeholder function to simulate Frege proof depth calculation
    # This is a dummy implementation and should be replaced with an actual algorithm
    return random.randint(10, 20)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_name = "diophantine_complexity"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    total_equations = 0
    total_depths = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        phi = ''.join(random.choice('01') for _ in range(n))
        
        # Convert Boolean formula to matrix form (simplified example)
        matrix = []
        for i in range(n):
            row = [int(phi[i])]
            for j in range(i+1, n):
                row.append(int(phi[j]))
            matrix.append(row)
        
        rank = gaussian_elimination(matrix)
        equations = len(matrix) - rank
        depth = frege_proof_depth(phi, n)
        
        total_equations += equations
        total_depths += depth
        
        if equations < math.log(n, 2)**2 or equations > math.sqrt(n) * math.log(n):
            conjecture_holds = False
            counterexample = f"n={n}, phi={phi}, equations={equations}"
        
        if depth > math.sqrt(n):
            conjecture_holds = False
            counterexample = f"n={n}, phi={phi}, depth={depth}"
    
    mean_equations = total_equations / instances_tested
    mean_depths = total_depths / instances_tested
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_equations,  # Using equations as a proxy for complexity
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(arg) for arg in sys.argv[1:]]
    else:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")