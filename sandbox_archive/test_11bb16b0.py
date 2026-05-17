# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import permutations, combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def perm_q(M):
        n = len(M)
        T_M = [sigma for sigma in permutations(n) if all(M[i][sigma[i]] == 1 for i in range(n))]
        return sum(2 ** maj(sigma) for sigma in T_M), len(T_M)
    
    def det_q(M):
        n = len(M)
        T_M = [sigma for sigma in permutations(n) if all(M[i][sigma[i]] == 1 for i in range(n))]
        return sum((-1) ** maj(sigma) * 2 ** maj(sigma) for sigma in T_M), len(T_M)
    
    def maj(sigma):
        descents = [i for i in range(1, n) if sigma[i-1] > sigma[i]]
        return sum(descents)
    
    def generate_matrix(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    results = []
    for n in [3, 4, 5, 6, 7, 8, 9, 10]:
        if n * (n - 1) // 2 < 2:
            continue
        
        perm_min_ratio = float('inf')
        
        for _ in range(30):
            M = generate_matrix(n)
            T_M_size = sum(all(M[i][sigma[i]] == 1 for i in range(n)) for sigma in permutations(n))
            if T_M_size < 2:
                continue
            
            perm_2, det_2 = perm_q(M), det_q(M)
            R_2 = perm_2 / max(1, abs(det_2))
            
            results.append({
                "n": n,
                "perm_2": perm_2,
                "det_2": det_2,
                "R_2": R_2
            })
            
            if R_2 < sqrt(T_M_size) / (2 * n):
                return {
                    "metric_name": "cancellation_ratio",
                    "metric_value": R_2,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, M={M}"
                }
            
            perm_min_ratio = min(perm_min_ratio, R_2)
        
        if perm_min_ratio >= sqrt(T_M_size) / (2 * n):
            return {
                "metric_name": "cancellation_ratio",
                "metric_value": perm_min_ratio,
                "instances_tested": 30,
                "conjecture_holds": True,
                "counterexample": ""
            }
    
    return {
        "metric_name": "cancellation_ratio",
        "metric_value": sum(result["R_2"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["R_2"] >= sqrt(T_M_size) / (2 * n) for result in results),
        "counterexample": ""
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
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")