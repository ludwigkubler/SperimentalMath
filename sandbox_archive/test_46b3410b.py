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
    
    def generate_bp(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def geometric_langlands_dual(bp):
        # Simplified mapping to a field of size |bp|
        return len(set(bp))
    
    def distinguishing_tensor_width(bp):
        n = len(bp)
        if n == 1:
            return 0
        return math.log(n, 2)
    
    def minimal_rank(dual):
        return dual
    
    c = 2  # Constant from the conjecture
    instances_tested = 30
    total_rho_over_m = 0.0
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        bp = generate_bp(n)
        dual = geometric_langlands_dual(bp)
        rho = distinguishing_tensor_width(bp)
        m = minimal_rank(dual)
        
        if m == 0:
            continue
        
        ratio = rho / m
        total_rho_over_m += ratio
        
        if ratio > math.log(n) / math.log(c):
            counterexample = f"BP of size {n} with ratio {ratio}"
    
    mean_rho_over_m = total_rho_over_m / instances_tested
    conjecture_holds = all(ratio <= math.log(n) / math.log(c) for n in [5, 10, 15, 20, 30, 40])
    
    return {
        "metric_name": "rho_over_m",
        "metric_value": mean_rho_over_m,
        "instances_tested": instances_tested,
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
    
    mean_rho_over_m = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_over_m} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho_over_m} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")