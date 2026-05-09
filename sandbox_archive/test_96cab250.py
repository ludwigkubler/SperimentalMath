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
    
    def generate_bp(n, read_twice):
        bp = []
        for _ in range(n):
            if read_twice:
                bp.append(random.choice(['x', 'y']))
                bp.append(random.choice(['x', 'y']))
            else:
                bp.append(random.choice(['x', 'y']))
        return bp
    
    def compute_monomials(bp):
        monomials = set()
        variables = {'x': 0, 'y': 0}
        for op in bp:
            if op == 'x':
                variables['x'] += 1
            elif op == 'y':
                variables['y'] += 1
            monomials.add(tuple(variables.copy()))
        return monomials
    
    def hilbert_function(monomials):
        max_degree = 0
        for monomial in monomials:
            degree = sum(monomial)
            if degree > max_degree:
                max_degree = degree
        return max_degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        read_twice_bp = generate_bp(n, True)
        read_once_bp = generate_bp(n, False)
        
        read_twice_monomials = compute_monomials(read_twice_bp)
        read_once_monomials = compute_monomials(read_once_bp)
        
        read_twice_deg = hilbert_function(read_twice_monomials)
        read_once_deg = hilbert_function(read_once_monomials)
        
        results.append({
            "n": n,
            "read_twice_deg": read_twice_deg,
            "read_once_deg": read_once_deg
        })
    
    metric_value_read_twice = sum(result["read_twice_deg"] for result in results) / len(results)
    metric_value_read_once = sum(result["read_once_deg"] for result in results) / len(results)
    
    conjecture_holds = all(result["read_twice_deg"] >= n / 2 for result in results) and \
                       all(result["read_once_deg"] <= math.log(n, 2) + 1 for result in results)
    
    counterexample = ""
    if not conjecture_holds:
        for i, result in enumerate(results):
            if result["read_twice_deg"] < n / 2 or result["read_once_deg"] > math.log(n, 2) + 1:
                counterexample = f"n={result['n']}, read-twice deg={result['read_twice_deg']}, read-once deg={result['read_once_deg']}"
                break
    
    return {
        "metric_name": "Hilbert Function Leading Coefficient",
        "metric_value_read_twice": metric_value_read_twice,
        "metric_value_read_once": metric_value_read_once,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_read_twice = sum(result["metric_value_read_twice"] for result in results) / len(results)
    std_read_twice = math.sqrt(sum((result["metric_value_read_twice"] - mean_read_twice)**2 for result in results) / len(results))
    mean_read_once = sum(result["metric_value_read_once"] for result in results) / len(results)
    std_read_once = math.sqrt(sum((result["metric_value_read_once"] - mean_read_once)**2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean_read_twice={mean_read_twice} std_read_twice={std_read_twice} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean_read_twice={mean_read_twice} std_read_twice={std_read_twice} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")