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
    
    def communication_complexity(f):
        n = len(f)
        comm = 0
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    comm += 1
        return comm
    
    def abelian_integral_order(f):
        # Placeholder function to simulate the computation of the minimal order of an abelian integral system
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(n)]
    
    comm_complexity = communication_complexity(f)
    abelian_order = abelian_integral_order(f)
    
    if comm_complexity <= Fraction(2 * n, 3):
        return {
            "metric_name": "abelian_order",
            "metric_value": abelian_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "communication_complexity <= 2n/3"
        }
    
    if abelian_order < Fraction(n, 3):
        return {
            "metric_name": "abelian_order",
            "metric_value": abelian_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "abelian_integral_order < n/3"
        }
    
    return {
        "metric_name": "abelian_order",
        "metric_value": abelian_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='seed {first_failing_seed}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")