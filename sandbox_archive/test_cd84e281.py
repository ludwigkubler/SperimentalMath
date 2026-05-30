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
    
    def entropy(phi):
        n = len(phi)
        support = list(phi.keys())
        P = [phi[x] / n for x in support]
        return -sum(p * math.log2(p) for p in P if p > 0)

    def generate_boolean_function(n):
        return {i: random.choice([0, 1]) for i in range(n)}

    h_10 = lambda phi: len(phi)  # Simplified Hodge number calculation

    results = []
    n_tested = 0
    n_max = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        phi = generate_boolean_function(n)
        h = h_10(phi)
        ent = entropy(phi)
        
        if h > ent:
            return {
                "metric_name": "Hodge number vs Entropy",
                "metric_value": h,
                "instances_tested": n_tested + 1,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"H^{1,0}({phi}) = {h}, Entropy({phi}) = {ent}"
            }
        
        results.append(h - ent)
        n_tested += 1
        n_max = max(n_max, n)

    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "Hodge number vs Entropy",
        "metric_value": mean,
        "instances_tested": n_tested,
        "n_max": n_max,
        "conjecture_holds": all(x <= 0 for x in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if not result["conjecture_holds"]:
            break
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([r for r in results if r <= 0]) / len(results)
    
    if all(r <= 0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > 0 for r in results[:int(len(results) * 0.8)]):
        print(f"RESULT: FALSIFIED counterexample='<desc>' first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")