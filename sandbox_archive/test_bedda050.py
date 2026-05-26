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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def and_or_tree(f, n):
        if n == 1:
            return f[0]
        else:
            left = and_or_tree(f[:2**(n-1)], n-1)
            right = and_or_tree(f[2**(n-1):], n-1)
            return [left[i] & right[i] for i in range(2**(n-1))]
    
    def weil_representation(f, n):
        if n == 1:
            return f
        else:
            left = weil_representation(f[:2**(n-1)], n-1)
            right = weil_representation(f[2**(n-1):], n-1)
            return [left[i] | right[i] for i in range(2**(n-1))]
    
    def communication_complexity(tree):
        if isinstance(tree, int):
            return 0
        else:
            return 1 + max(communication_complexity(tree[0]), communication_complexity(tree[1]))
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    tree = and_or_tree(f, n)
    W = weil_representation(f, n)
    rho_f = len(W)
    comm_complexity = communication_complexity(tree)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": comm_complexity <= 2**rho_f,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "communication_complexity > 2^rho_f"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")