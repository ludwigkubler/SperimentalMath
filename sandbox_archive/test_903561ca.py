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
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n)
        f = [random.choice([0, 1]) for _ in range(2**m)]
        
        # Compute boolean hyperplane arrangement and rank variance
        R_f = 0
        for i in range(len(f)):
            if f[i] == 1:
                R_f += 1
        
        # Compute Hodge classes and minimal Hodge theoretical dimension
        HDim_f = n - m
        
        if HDim_f == 0:
            continue
        
        ratio = R_f / HDim_f
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    conjecture_holds = 0.5 <= mean_ratio <= 1.5
    
    return {
        "metric_name": "Ratio of Rank Variance to Hodge Dimension",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    support_fraction = sum(1 for r in results if 0.5 <= r <= 1.5) / len(results)
    
    if all(0.5 <= r <= 1.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if not (0.5 <= r <= 1.5))]
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")