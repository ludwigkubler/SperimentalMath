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
    
    def generate_read_twice_bp(n):
        bp = []
        for _ in range(n):
            if random.choice([0, 1]) == 0:
                bp.append(random.choice([0, 1]))
            else:
                bp.append(generate_read_twice_bp(2))
        return bp
    
    def compute_tropical_curve(bp):
        # Simplified tropical curve computation for demonstration
        return [sum(x) % 2 for x in bp]
    
    def rank(tropical_curve):
        n = len(tropical_curve)
        if n == 0:
            return 0
        max_rank = 1
        for i in range(n):
            row = tropical_curve[i]
            col = [tropical_curve[j][i] for j in range(n)]
            if sum(row) > max_rank:
                max_rank = sum(row)
            if sum(col) > max_rank:
                max_rank = sum(col)
        return max_rank
    
    def log_size(bp):
        size = 1
        for x in bp:
            if isinstance(x, list):
                size *= log_size(x)
            else:
                size += 1
        return math.log(size, 2)
    
    n = random.randint(5, 40)
    bp = generate_read_twice_bp(n)
    tropical_curve = compute_tropical_curve(bp)
    rank_value = rank(tropical_curve)
    log_size_value = log_size(bp)
    
    if bp == [0] * n:
        conjecture_holds = False
        counterexample = "IP_2"
    else:
        c = 1.5  # Example constant, adjust as needed
        if rank_value <= c * log_size_value and rank_value >= n / c:
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = "Rank does not match expected bounds"
    
    return {
        "metric_name": "Rank vs Log Size",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")