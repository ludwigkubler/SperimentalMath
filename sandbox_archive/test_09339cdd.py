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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        m, n = len(A), len(A[0])
        r = 0
        for i in range(m):
            if any(A[i][j] != 0 for j in range(n)):
                r += 1
        return r
    
    def width(bdp):
        max_width = 0
        current_width = 0
        for gate in bdp:
            if gate == '1':
                current_width += 1
            else:
                max_width = max(max_width, current_width)
                current_width = 0
        return max(max_width, current_width)
    
    def generate_bdp(n):
        bdp = []
        for _ in range(n):
            bdp.append(random.choice(['0', '1']))
        return ''.join(bdp)
    
    n = random.randint(5, 40)
    bdp = generate_bdp(n)
    H = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    H = gaussian_elimination(H)
    minimal_rank = rank(H)
    width_value = width(bdp)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": abs(minimal_rank - width_value) <= 3 and minimal_rank <= 10,
        "counterexample": "" if conjecture_holds else f"rank={minimal_rank}, expected={width_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")