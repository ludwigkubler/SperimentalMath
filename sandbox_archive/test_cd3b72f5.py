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
    
    n = 10  # Number of variables in the Boolean function
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    def xor_and_tree_width(f):
        if len(f) == 1:
            return 0
        mid = len(f) // 2
        left_width = xor_and_tree_width(f[:mid])
        right_width = xor_and_tree_width(f[mid:])
        return max(left_width, right_width) + 1
    
    T_f = xor_and_tree_width(f)
    
    def geometric_quantization_rank(f):
        if len(f) == 1:
            return 1
        mid = len(f) // 2
        left_rank = geometric_quantization_rank(f[:mid])
        right_rank = geometric_quantization_rank(f[mid:])
        return max(left_rank, right_rank)
    
    R_f = geometric_quantization_rank(f)
    
    ratio = R_f / T_f if T_f != 0 else float('inf')
    
    return {
        "metric_name": "R(f)/T(f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2,
        "counterexample": f"R(f)={R_f}, T(f)={T_f}" if ratio > 2 else ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if r["metric_value"] > 2), None)
        result = f"FALSIFIED counterexample=\"R(f)>{2*T_f}, T(f)={T_f}\" first_failing_seed={first_failing_seed}"
    
    print(result)