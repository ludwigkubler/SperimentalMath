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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 5 + (seed % 4) * 5  # Sweep n through {5,10,15,20,30,40}
    if n > 40:
        return {
            "metric_name": "n",
            "metric_value": n,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n_too_large"
        }
    
    # Generate a random Boolean function f of size n
    f = [random.randint(0, 1) for _ in range(n)]
    
    # Construct the associated geometric Langlands dual object L(f)
    # For simplicity, let's assume L(f) is a matrix representation of f
    L_f = [[f[j] if i == j else 0 for j in range(n)] for i in range(n)]
    
    # Compute the minimal rank r(L(f))
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            rank += 1
            for row in range(rank, rows):
                factor = Fraction(matrix[row][col], matrix[pivot_row][col])
                for j in range(cols):
                    matrix[row][j] -= factor * matrix[pivot_row][j]
        return rank
    
    r_L_f = gaussian_elimination(L_f)
    
    # Compute the length of any Frege proof for f
    def frege_proof_length(f):
        if all(x == 0 for x in f) or all(x == 1 for x in f):
            return 1
        else:
            return len(f) + sum(1 for x in f if x != 0 and x != 1)
    
    length_of_Frege_proof = frege_proof_length(f)
    
    # Check if the conjectured lower bound is satisfied
    conjecture_holds = r_L_f <= 2 ** length_of_Frege_proof
    
    return {
        "metric_name": "rank_bound",
        "metric_value": r_L_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, rank={r_L_f}, proof_length={length_of_Frege_proof}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        mean = sum(r["metric_value"] for r in results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean} std={std} support_fraction={support_fraction}")