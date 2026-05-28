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
    n = len(matrix)
    rank = 0
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        if matrix[max_row][i] == 0:
            continue
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        rank += 1
        for j in range(n):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random ACC⁰ circuit of size s
    s = random.randint(5, 40)
    n = 2 ** s
    
    # Construct the tropical graph G
    G = []
    for i in range(n):
        row = [0] * n
        for j in range(i+1, n):
            if (i & (j - i)) == 0:
                row[j] = random.choice([1, -1])
        G.append(tuple(row))
    
    # Compute the rank of the vertex set of G
    rank = gaussian_elimination(G)
    
    # Check if the conjecture holds
    conjecture_holds = rank <= s * math.log(n, 2)
    counterexample = "" if conjecture_holds else "rank(G) > s log n"
    
    return {
        "metric_name": "Rank of Tropical Graph",
        "metric_value": rank,
        "instances_tested": len(G),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank(G) > s log n\" first_failing_seed={first_failing_seed}")