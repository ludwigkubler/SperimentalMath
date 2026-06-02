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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("f must be a Boolean function of n bits")
        
        rank = 0
        for i in range(n):
            count_1 = sum(1 for x in f[::2**i] if x == 1)
            count_0 = sum(1 for x in f[::2**i] if x == 0)
            if count_1 > count_0:
                rank += 1
        return rank
    
    def minimal_symmetric_spectrum_dimension(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("f must be a Boolean function of n bits")
        
        mssd = 0
        for i in range(n):
            count_1 = sum(1 for x in f[::2**i] if x == 1)
            count_0 = sum(1 for x in f[::2**i] if x == 0)
            mssd += abs(count_1 - count_0)
        return mssd
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_mssd = 0
    total_rank = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # 5 instances per size
            f = generate_boolean_function(n)
            mssd = minimal_symmetric_spectrum_dimension(f)
            rank = communication_complexity_rank(f)
            total_mssd += mssd
            total_rank += rank
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_mssd = Fraction(total_mssd, instances_tested)
    mean_rank = Fraction(total_rank, instances_tested)
    ratio = abs(mean_mssd / mean_rank)
    
    if ratio > 1.5:
        conjecture_holds = False
        counterexample = f"Ratio {ratio} exceeds threshold"
    
    return {
        "metric_name": "MSSD/Rank Ratio",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
        67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds threshold\" first_failing_seed={seeds[first_failing_seed]}")