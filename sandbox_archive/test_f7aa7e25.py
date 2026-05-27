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
            if A[i][i] == 0:
                continue
            for j in range(n-1, i-1, -1):
                A[i][j] /= A[i][i]
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def hodge_rank(f, p):
        n = len(f)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                A[i][j] = sum((f[k] ** (i+j-k)) % p for k in range(n+1)) % p
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def min_refutation_size(f, p):
        n = len(f)
        literals = list(range(n))
        refutations = []
        
        def backtrack(literals):
            if not literals:
                refutations.append([f])
                return
            x = literals[0]
            for i in range(p):
                f[x] = i
                backtrack(literals[1:])
        
        backtrack(literals)
        min_size = float('inf')
        for refutation in refutations:
            size = sum(1 for clause in refutation if any(abs(coeff) > 0 for coeff in clause))
            if size < min_size:
                min_size = size
        return min_size
    
    n = random.randint(5, 40)
    p = random.choice([2, 3, 5, 7, 11])
    f = [random.randint(0, p-1) for _ in range(n+1)]
    
    hodge_r = hodge_rank(f, p)
    ref_size = min_refutation_size(f, p)
    
    if ref_size == float('inf'):
        return {
            "metric_name": "Hodge Rank",
            "metric_value": hodge_r,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_ref_size = math.log(ref_size, p)
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": hodge_r,
        "instances_tested": 1,
        "conjecture_holds": hodge_r >= log_ref_size,
        "counterexample": "" if hodge_r >= log_ref_size else f"Counterexample: n={n}, p={p}, f={f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j + 5**k for i in range(5) for j in range(5) for k in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "counterexample" in r for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and "counterexample" in r)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"] and "counterexample" in r)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples")