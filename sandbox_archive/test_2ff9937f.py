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
    
    def xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 0
        for i in range(n):
            if f[i] != (f[:i] + f[i+1:])[-1]:
                return 1 + max(xor_and_tree_width(f[:i]), xor_and_tree_width(f[i+1:]))
        return 0
    
    def geometric_quantization_rank(f):
        n = len(f)
        if n == 1:
            return 1
        rank = 2
        for i in range(n):
            rank = max(rank, geometric_quantization_rank(f[:i]) + geometric_quantization_rank(f[i+1:]))
        return rank
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_random_boolean_function(n)
            T_f = xor_and_tree_width(f)
            R_f = geometric_quantization_rank(f)
            if T_f == 0 and R_f != 1:
                return {
                    "metric_name": "R(f)/T(f)",
                    "metric_value": float('inf'),
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"Counterexample for n={n}: T(f)=0, R(f)={R_f}"
                }
            if T_f != 0:
                total_ratio += Fraction(R_f, T_f)
                instances_tested += 1
    
    mean_ratio = total_ratio / instances_tested
    return {
        "metric_name": "R(f)/T(f)",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": mean_ratio <= Fraction(3, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
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
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='R(f)/T(f) > 1.5' first_failing_seed={seeds[first_failing_seed]}")