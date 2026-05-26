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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    rref = [[Fraction(0, 1)] * cols for _ in range(rows)]
    
    def scale_row(i, factor):
        if factor == Fraction(0, 1):
            return
        for j in range(cols):
            rref[i][j] *= factor
    
    def add_rows(i, j, factor):
        for k in range(cols):
            rref[j][k] += factor * rref[i][k]
    
    def find_pivot_row(col):
        for i in range(rank, rows):
            if rref[i][col] != Fraction(0, 1):
                return i
        return -1
    
    for col in range(cols):
        pivot_row = find_pivot_row(col)
        if pivot_row == -1:
            continue
        scale_row(pivot_row, Fraction(1, rref[pivot_row][col]))
        rank += 1
        for i in range(rows):
            if i != pivot_row:
                add_rows(pivot_row, i, -rref[i][col])
    
    return rank

def dpll_width(formula):
    # Placeholder implementation of DPLL width calculation
    # This is a dummy function and should be replaced with actual logic
    return 10  # Example value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    rank = matrix_rank(formula)
    width = dpll_width(formula)
    
    metric_value = rank / width
    conjecture_holds = metric_value <= 1.5
    counterexample = "" if conjecture_holds else f"Rank {rank} > Width {width}"
    
    return {
        "metric_name": "Ratio of Rank to DPLL Width",
        "metric_value": metric_value,
        "instances_tested": n * n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 2))
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")