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

def generate_ac0_circuit(n, s):
    if n == 1:
        return [random.choice([0, 1])]
    elif s == 1:
        return [random.choice([0, 1])]
    
    left = generate_ac0_circuit(n // 2, s // 2)
    right = generate_ac0_circuit(n // 2, s - s // 2)
    
    if len(left) != len(right):
        raise ValueError("Left and right circuits must have the same length")
    
    return [left[i] | right[i] for i in range(len(left))]

def compute_polynomial_system(circuit):
    n = len(circuit)
    m = 1 << n
    P = []
    
    for i in range(m):
        term = 0
        for j in range(n):
            if (i >> j) & 1:
                term |= circuit[j]
        P.append(term)
    
    return P

def min_tropical_growth_rate(P):
    max_p = max(P)
    if max_p == 0:
        return 0
    return math.log2(max_p)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for s in range(1, min(n + 1, 41)):
            try:
                circuit = generate_ac0_circuit(n, s)
                P = compute_polynomial_system(circuit)
                g_P = min_tropical_growth_rate(P)
                results.append((n, s, g_P))
            except Exception as e:
                return {
                    "metric_name": "minimal_tropical_growth_rate",
                    "metric_value": None,
                    "instances_tested": 0,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
    
    if not results:
        return {
            "metric_name": "minimal_tropical_growth_rate",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    total_g_P = sum(g_P for _, _, g_P in results)
    instances_tested = len(results)
    
    mean_g_P = total_g_P / instances_tested
    conjecture_holds = all(g_P >= math.log2(s) for _, s, g_P in results)
    
    return {
        "metric_name": "minimal_tropical_growth_rate",
        "metric_value": mean_g_P,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(results):
        return
    
    mean_g_P = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_g_P} std=NA support_fraction={support_fraction}")
    elif support_fraction < 0.7:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='g(P) < c·log(s)' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")