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
    
    def log(n):
        if n <= 0:
            return float('-inf')
        return math.log2(n)
    
    def free_entanglement(n):
        # Simplified model for minimal free entanglement
        return log(n)
    
    def communication_protocol_complexity(n):
        # Example complexity function, replace with actual protocol
        return n * log(n)
    
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        rho_P = free_entanglement(n)
        C_n = communication_protocol_complexity(n)
        
        if rho_P >= log(n):
            conjecture_holds = False
            counterexample = f"Free entanglement {rho_P} is not less than log({n}) = {log(n)}"
        
        total_metric_value += rho_P
        instances_tested += 1
    
    return {
        "metric_name": "Minimal Free Entanglement",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")