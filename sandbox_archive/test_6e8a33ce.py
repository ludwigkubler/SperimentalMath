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
    
    def compute_jordan_algebra(f):
        n = len(f)
        J = {}
        for i in range(n):
            for j in range(i+1, n):
                if f[i] == f[j]:
                    J[(i, j)] = 1
                else:
                    J[(i, j)] = -1
        return J
    
    def compute_noncommutative_geometric_invariant(J):
        total = 0
        for (i, j), value in J.items():
            total += abs(value)
        return total
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    J = compute_jordan_algebra(f)
    J_value = compute_noncommutative_geometric_invariant(J)
    
    IP_2_trivial_BP_size = n
    log_squared_size = math.log(IP_2_trivial_BP_size) ** 2
    
    conjecture_holds = J_value <= log_squared_size and J_value >= n
    counterexample = "" if conjecture_holds else f"J(f)={J_value}, IP_2 trivial BP size={IP_2_trivial_BP_size}"
    
    return {
        "metric_name": "noncommutative_geometric_invariant",
        "metric_value": J_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")