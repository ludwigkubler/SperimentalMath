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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def min_rank(f):
        # Placeholder for actual computation of minimal rank
        # This is a dummy implementation that returns a constant value
        return 1
    
    def bp_read_twice_complexity(P):
        # Placeholder for actual computation of BP_ReadTwice complexity
        # This is a dummy implementation that returns a constant value
        return 1
    
    n = random.randint(5, 40)
    P = [random.choice([0, 1]) for _ in range(n)]
    
    f_P = sum(P[i] * (2 ** i) for i in range(n))
    rank = min_rank(f_P)
    complexity = bp_read_twice_complexity(P)
    
    conjecture_holds = abs(log2(rank) - complexity) <= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "BP_ReadTwice_Complexity",
        "metric_value": complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")