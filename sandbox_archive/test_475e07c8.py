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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        if k > n:
            return 0
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def major_index(sigma):
        descents = sum(1 for i in range(len(sigma) - 1) if sigma[i] > sigma[i + 1])
        return descents
    
    def perm_q(M, q=2):
        n = len(M)
        T_M = [sigma for sigma in permutations(n) if all(M[i][sigma[i]] == 1 for i in range(n))]
        return sum(q ** major_index(sigma) for sigma in T_M)
    
    def det_q(M, q=2):
        n = len(M)
        T_M = [sigma for sigma in permutations(n) if all(M[i][sigma[i]] == 1 for i in range(n))]
        sign_sigma = lambda sigma: sum(1 if (i < j and M[i][j] == 0) else -1 for i, j in combinations(sigma))
        return sum(sign_sigma(sigma) * q ** major_index(sigma) for sigma in T_M)
    
    def permutations(n):
        if n == 0:
            yield []
        elif n == 1:
            yield [0]
        else:
            for perm in permutations(n - 1):
                for i in range(n):
                    new_perm = perm[:i] + [n - 1] + perm[i:i]
                    yield new_perm
    
    def combinations(iterable, r):
        pool = list(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i + 1, r):
                indices[j] = indices[j - 1] + 1
            yield tuple(pool[i] for i in indices)
    
    n_values = [3, 4, 5, 6, 7, 8, 9, 10]
    results = []
    min_ratio = float('inf')
    
    for n in n_values:
        M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        T_M_size = sum(all(M[i][j] == 1 for i in range(n)) for j in range(n))
        if T_M_size < 2:
            continue
        
        perm_2 = perm_q(M)
        det_2 = det_q(M)
        R_2 = perm_2 / max(1, abs(det_2))
        
        results.append({
            "n": n,
            "perm_2": perm_2,
            "det_2": det_2,
            "R_2": R_2,
            "T_M_size": T_M_size
        })
        
        min_ratio = min(min_ratio, R_2)
    
    if all(R_2 >= math.sqrt(T_M_size) / (2 * n) for r in results):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "R_2(M) < sqrt(|T_M|)/(2n)"
    
    return {
        "metric_name": "cancellation_ratio",
        "metric_value": min_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")