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
    
    def hypergeometric_function(n, k):
        return sum(math.comb(n, i) * (-1)**i for i in range(k+1)) / math.comb(2*n, n)
    
    def moments_of_hypergeometric(f, k):
        return [f**i for i in range(k+1)]
    
    def log_power(n, power):
        return math.log(n) ** power
    
    def ac0_circuit_size(depth):
        # Simplified model of AC0 circuit size
        return 2 ** depth
    
    n_max = 40
    k_max = int(math.log2(n_max)) ** 2
    results = []
    
    for n in range(5, n_max + 1):
        size_C = ac0_circuit_size(int(math.log2(n)))
        moments_sum = sum(moments_of_hypergeometric(hypergeometric_function(n, k), k) for k in range(k_max + 1))
        ratio = moments_sum / log_power(size_C, k_max)
        
        results.append({
            "n": n,
            "size_C": size_C,
            "moments_sum": moments_sum,
            "ratio": ratio
        })
    
    conjecture_holds = all(abs(ratio - math.log2(n)) <= 1 for r in ratios for n in range(5, n_max + 1))
    counterexample = "" if conjecture_holds else f"Ratio {ratio} does not match expected log^k(size(C))"
    
    return {
        "metric_name": "Ratio of Moments to Log^k(Size(C))",
        "metric_value": sum(r["ratio"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")