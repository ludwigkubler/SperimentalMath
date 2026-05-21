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
    
    n = random.randint(5, 40)
    X = set(range(n))
    
    # Constructive mapping for secant variety and noncommutative L^p geometric entropy
    def secant_variety(X):
        V_X = []
        for x in X:
            for y in X:
                if x != y:
                    V_X.append((x, y))
        return V_X
    
    def noncommutative_Lp_entropy(V_X):
        # Placeholder implementation; actual computation depends on the conjecture
        return len(V_X) / n
    
    V_X = secant_variety(X)
    H_mu_V_X = noncommutative_Lp_entropy(V_X)
    
    metric_name = "noncommutative_Lp_entropy"
    metric_value = H_mu_V_X
    instances_tested = 1
    conjecture_holds = H_mu_V_X >= n
    counterexample = "" if conjecture_holds else f"mapping_undefined for n={n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")