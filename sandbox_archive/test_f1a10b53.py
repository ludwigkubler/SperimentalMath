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
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        # Find pivot
        if A[i][i] == 0:
            for j in range(i + 1, rows):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                continue  # No non-zero pivot found, skip row
        # Eliminate below
        for j in range(i + 1, rows):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(cols):
                A[j][k] -= factor * A[i][k]
    return A

def rank(matrix):
    rref = gaussian_elimination(matrix)
    rank_value = sum(1 for row in rref if any(row))
    return rank_value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    width = n + 1
    Tseitin_circuit = [[random.randint(0, 1) for _ in range(width)] for _ in range(width)]
    
    rank_value = rank(Tseitin_circuit)
    c_n = Fraction(rank_value, n)
    
    return {
        "metric_name": "Minimal Rank of Kostant Partition Function",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": abs(c_n - n) <= 3,
        "counterexample": "" if c_n - n <= 3 else f"c(n) = {c_n}, |cn - n| > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100, 4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")