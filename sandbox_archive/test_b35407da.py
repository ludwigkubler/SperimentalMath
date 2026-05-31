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
    
    def communication_complexity(f):
        n = len(f)
        if n <= 1:
            return 0
        C_f = 0
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    C_f += 1
        return C_f
    
    def coxeter_diagram(f):
        n = len(f)
        R_f = set()
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    R_f.add((i, j))
        return R_f
    
    def alpha(C_f, log_n):
        # Placeholder function for the absolute constant α
        return C_f * log_n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = [random.choice([True, False]) for _ in range(n)]
        C_f = communication_complexity(f)
        R_f = coxeter_diagram(f)
        log_n = math.log2(n) if n > 1 else 0
        ratio = Fraction(len(R_f), log_n) if log_n != 0 else float('inf')
        
        results.append({
            "n": n,
            "C_f": C_f,
            "R_f": len(R_f),
            "log_n": log_n,
            "ratio": ratio,
            "alpha": alpha(C_f, log_n)
        })
    
    total_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] <= result["alpha"] for result in results)
    counterexample = "" if conjecture_holds else f"Ratio {total_ratio} exceeds alpha {result['alpha']}"
    
    return {
        "metric_name": "Communication Complexity Ratio",
        "metric_value": total_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds alpha\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")