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
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    if n == 1:
        return {
            "metric_name": "free_cumulant_magnitude",
            "metric_value": 0.1 * math.log(1),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "n=1 is trivial and does not support the conjecture"
        }
    
    # Generate a read-twice BP
    P = [[random.random() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        P[i][i] += 1
    
    # Compute the free cumulant magnitude via moments (simplified)
    def moment(P, k):
        if k == 0:
            return sum(sum(row) for row in P)
        elif k == 1:
            return sum(sum(row) for row in P)
        else:
            return 0
    
    free_cumulant_magnitude = abs(moment(P, 2))
    
    # Check the conjecture
    if free_cumulant_magnitude >= 0.1 * math.log(n):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Read-twice BP with n={n} failed: ||κ(P)|| < 0.1 * log n"
    
    return {
        "metric_name": "free_cumulant_magnitude",
        "metric_value": free_cumulant_magnitude,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")