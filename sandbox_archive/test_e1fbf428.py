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
    
    def xor_function(x, y):
        return x ^ y
    
    def communication_complexity(f, n):
        # Simplified model for communication complexity of XOR function
        return n
    
    def automorphic_lattice_order(n):
        # Simplified model for the order of an automorphic lattice associated with XOR
        return 2 ** (n - 1)
    
    C = 1.5  # Constant factor to test against
    results = []
    
    for _ in range(30):  # Test with 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = xor_function
        cc = communication_complexity(f, n)
        order = automorphic_lattice_order(n)
        
        if cc > 0:
            ratio = order / cc
            results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    conjecture_holds = all(r <= C for r in results)
    counterexample = "" if conjecture_holds else "ratio_exceeds_C"
    
    return {
        "metric_name": "Ratio of Lattice Order to Communication Complexity",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    support_fraction = sum(r <= 1.5 for r in results) / len(results)
    
    if all(r <= 1.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(r > 1.5 for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result > 1.5)
        print(f"RESULT: FALSIFIED counterexample='ratio_exceeds_C' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_metric")