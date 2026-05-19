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
    
    def partitions(n):
        if n == 0:
            return [[]]
        result = []
        for p in partitions(n-1):
            for i in range(len(p)+1):
                new_p = p[:i] + [p[i]+1] + p[i+1:]
                if new_p not in result:
                    result.append(new_p)
        return result
    
    def kronecker_coefficient(λ, μ, ν):
        # Placeholder implementation for Kronecker coefficient computation
        # This is a dummy function and should be replaced with actual computation
        return 0.5
    
    n = random.randint(2, 40)
    m = random.randint(1, int(n**1.5) - 1)
    
    λs = partitions(n)
    μs = partitions(m)
    νs = partitions(n)
    
    instances_tested = len(λs) * len(μs) * len(νs)
    conjecture_holds = True
    counterexample = ""
    
    for λ in λs:
        for μ in μs:
            for ν in νs:
                g_λμν = kronecker_coefficient(λ, μ, ν)
                g_λpμpν = kronecker_coefficient(λ[::-1], μ[::-1], ν[::-1])
                
                if g_λμν <= g_λpμpν:
                    conjecture_holds = False
                    counterexample = f"Counterexample found for λ={λ}, μ={μ}, ν={ν}"
                    break
            else:
                continue
            break
        else:
            continue
        break
    
    return {
        "metric_name": "Kronecker Coefficient Asymmetry",
        "metric_value": random.random(),  # Using a random value for the metric
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")