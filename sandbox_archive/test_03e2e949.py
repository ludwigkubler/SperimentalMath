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
    
    def tropicalize(f, n):
        return [f(2**i) for i in range(n)]
    
    def tensor_product_rank(tensors):
        if not tensors:
            return 0
        rank = len(tensors[0])
        for t in tensors[1:]:
            new_rank = 0
            for i in range(rank):
                for j in range(len(t)):
                    if all(t[i][k] + t[j][k] > -math.inf for k in range(len(t))):
                        new_rank += 1
                        break
            rank = new_rank
        return rank
    
    def log2_floor(x):
        return int(math.log2(x)) if x > 0 else -1
    
    n = random.randint(5, 40)
    f = lambda x: x**3 + 2*x + 1  # Example polynomial function
    T_f = tropicalize(f, n)
    R_min_T_f = tensor_product_rank(T_f)
    
    metric_value = R_min_T_f
    instances_tested = 1
    conjecture_holds = R_min_T_f >= log2_floor(n) ** 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "R_min(T_f)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")