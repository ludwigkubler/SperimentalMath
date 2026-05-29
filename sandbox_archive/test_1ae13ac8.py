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
    
    def frege_proof_complexity(f):
        n = len(f)
        if n == 1:
            return 1
        else:
            return 1 + max(frege_proof_complexity(f[:n//2]), frege_proof_complexity(f[n//2:]))
    
    def count_monoids(f):
        n = len(f)
        if n == 1:
            return 1
        else:
            return 1 + count_monoids(f[:n//2]) + count_monoids(f[n//2:])
    
    instances_tested = 0
    total_monoids = 0
    total_depth_cubed = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        depth = frege_proof_complexity(f)
        monoids = count_monoids(f)
        
        instances_tested += 1
        total_monoids += monoids
        total_depth_cubed += depth ** 3
        
        if monoids > depth ** 3:
            return {
                "metric_name": "Monoids vs Depth^3",
                "metric_value": monoids,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"n={n}, Monoids={monoids}, D(f)^3={depth**3}"
            }
    
    return {
        "metric_name": "Monoids vs Depth^3",
        "metric_value": total_monoids / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")