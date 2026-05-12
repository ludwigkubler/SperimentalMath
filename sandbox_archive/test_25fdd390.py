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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(n, k):
    if (n, k) not in memo_hook_lengths:
        memo_hook_lengths[(n, k)] = (n - k + 1) * factorial(n - 1) // (factorial(k) * factorial(n - k))
    return memo_hook_lengths[(n, k)]

def hook_length_tableau_count(n):
    total = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            total *= hook_length_formula(i, j)
    return factorial(n) // total

def run_trial(seed: int) -> dict:
    random.seed(seed)
    memo_hook_lengths = {}
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        λ_n = (n, n)
        μ_n = tuple(range(1, n + 1))
        
        SYT_λ_n = hook_length_tableau_count(n)
        SYT_μ_n = hook_length_tableau_count(n)
        
        ratio = SYT_λ_n / SYT_μ_n
        expected_ratio = 2 ** (n / 2)
        
        results.append({
            "n": n,
            "SYT_λ_n": SYT_λ_n,
            "SYT_μ_n": SYT_μ_n,
            "ratio": ratio,
            "expected_ratio": expected_ratio
        })
    
    conjecture_holds = all(ratio >= expected_ratio for r in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, SYT(λ_n)={results[0]['SYT_λ_n']}, SYT(μ_n)={results[0]['SYT_μ_n']}"
    
    return {
        "metric_name": "Hook-Length Ratio",
        "metric_value": sum(r["ratio"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")