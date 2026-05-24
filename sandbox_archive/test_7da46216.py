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
    
    def xor_function(n):
        return lambda x: sum(x[i] for i in range(n)) % 2
    
    def p_adic_order(f, p):
        if f(0) != 0:
            return 0
        n = 1
        while True:
            if f(p**n) == 0:
                n += 1
            else:
                break
        return n - 1
    
    def acc0_circuit_size(n):
        # Placeholder function for ACC⁰ circuit size calculation
        # This is a dummy implementation and should be replaced with an actual algorithm
        return 2**n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = xor_function(n)
        p = random.choice([2, 3, 5, 7, 11, 13, 17, 19])
        order = p_adic_order(f, p)
        S = acc0_circuit_size(n)
        
        results.append({
            "n": n,
            "order": order,
            "S": S
        })
    
    mean_order = sum(result["order"] for result in results) / len(results)
    support_fraction = all(result["order"] <= math.sqrt(result["n"]) and result["p"] >= 2**result["S"] for result in results)
    
    return {
        "metric_name": "Minimal p-Adic Order vs ACC⁰ Circuit Size",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")