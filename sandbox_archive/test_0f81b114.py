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
    
    def matroid_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if all(abs(A[i][j]) < 1e-9 for j in range(n)):
                continue
            pivot_col = next(j for j in range(n) if abs(A[i][j]) > 1e-9)
            A[i], A[rank] = A[rank], A[i]
            rank += 1
            for j in range(m):
                if j != i:
                    factor = A[j][pivot_col]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return rank
    
    def minimal_tropical_order(A):
        m, n = len(A), len(A[0])
        B = [[Fraction(1) if abs(A[i][j]) > 1e-9 else Fraction(0) for j in range(n)] for i in range(m)]
        B = gaussian_elimination(B)
        rank = matroid_rank(B)
        return rank
    
    def clause_complexity(phi):
        return len(phi.split(' ')) // 2
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        instances_tested = 0
        mto_sum = 0
        cc_sum = 0
        for _ in range(5):
            variables = set()
            phi = []
            for _ in range(n):
                clause = ' '.join(random.sample(variables, random.randint(1, len(variables))))
                phi.append(clause)
                variables.add(f'x{random.randint(1, 100)}')
            mto = minimal_tropical_order(phi)
            cc = clause_complexity(' '.join(phi))
            results.append({"mto": mto, "cc": cc})
            instances_tested += 1
        mto_values = [r["mto"] for r in results]
        cc_values = [r["cc"] for r in results]
        mto_mean = sum(mto_values) / len(mto_values)
        cc_mean = sum(cc_values) / len(cc_values)
        correlation = sum((mto - mto_mean) * (cc - cc_mean) for mto, cc in zip(mto_values, cc_values)) / (len(mto_values) * sum((mto - mto_mean)**2 for mto in mto_values))
        mean_abs_diff = sum(abs(mto - cc) for mto, cc in zip(mto_values, cc_values)) / len(mto_values)
        conjecture_holds = correlation >= 0.8 and mean_abs_diff <= 3
        counterexample = "" if conjecture_holds else "correlation<0.8 or mean_abs_diff>3"
        return {
            "metric_name": "minimal_tropical_order",
            "metric_value": mto_mean,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")