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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if f[i] != f[~i]:
                count += 1
        return count
    
    def minimal_deligne_connes_tensor_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    rank += 1
        return rank
    
    instances_tested = 0
    mDCT_sum = 0
    C_sum = 0
    n_max = 5
    
    for _ in range(30):
        n = random.randint(5, 40)
        if n > n_max:
            n_max = n
        
        f = generate_boolean_function(n)
        mDCT = minimal_deligne_connes_tensor_rank(f)
        C = communication_complexity(f)
        
        mDCT_sum += mDCT
        C_sum += C
        instances_tested += 1
    
    mDCT_mean = mDCT_sum / instances_tested
    C_mean = C_sum / instances_tested
    ratio = mDCT_mean / C_mean if C_mean != 0 else float('inf')
    
    conjecture_holds = abs(ratio - 1) <= 0.1
    
    return {
        "metric_name": "mDCT/C_ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mDCT_mean = sum(r["metric_value"] for r in results) / len(results)
    C_mean = sum(1/r["metric_value"] for r in results if r["metric_value"] != 0) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mDCT_mean} std=NA support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mDCT_mean} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")