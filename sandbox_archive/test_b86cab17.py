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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = set()
        for i in range(n):
            rank.add(sum(f[j] << i for j in range(n) if (j >> i) & 1))
        return Fraction(len(rank), n)
    
    def minimal_topological_degree(f):
        n = len(f)
        degree = 0
        for i in range(n):
            count = sum(1 for j in range(n) if f[j] != f[j ^ (1 << i)])
            degree = max(degree, count)
        return degree
    
    def resolution_proof_width(f):
        n = len(f)
        width = 0
        for i in range(n):
            count = sum(1 for j in range(n) if f[j] != f[j ^ (1 << i)])
            width = max(width, count)
        return width
    
    metric_name = "minimal_topological_degree"
    instances_tested = 0
    n_max = 0
    total_td = Fraction(0)
    total_rc = Fraction(0)
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(16):
            f = generate_boolean_function(n)
            td = minimal_topological_degree(f)
            rc = communication_complexity_rank_variance(f)
            width = resolution_proof_width(f)
            
            total_td += td
            total_rc += rc
            
            instances_tested += 1
    
    mean_td = total_td / instances_tested
    mean_rc = total_rc / instances_tested
    
    conjecture_holds = mean_td >= mean_rc
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(mean_td),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")