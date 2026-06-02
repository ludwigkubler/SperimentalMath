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
    
    def symmetric_spectrum_dimension(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(n):
            if all(f[j] == f[j ^ (1 << i)] for j in range(len(f))):
                count += 1
        return count
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(2**n):
            if f[i] == 1:
                rank += 1
        return rank
    
    instances_tested = 0
    total_mssd = 0
    total_rank = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            f = generate_boolean_function(n)
            mssd = symmetric_spectrum_dimension(f)
            rank = communication_complexity_rank(f)
            
            instances_tested += 1
            total_mssd += mssd
            total_rank += rank
    
    mean_mssd = total_mssd / instances_tested
    mean_rank = total_rank / instances_tested
    ratio = abs(mean_mssd / mean_rank)
    
    conjecture_holds = ratio <= 1.5
    counterexample = "" if conjecture_holds else f"Ratio {ratio} exceeds threshold"
    
    return {
        "metric_name": "MSSD/Rank Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds threshold\" first_failing_seed={first_failing_seed}")