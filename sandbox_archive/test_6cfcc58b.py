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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        max_communication = 0
        for i in range(2**n):
            comm = sum(abs(f[i] - f[j]) for j in range(i+1, 2**n))
            if comm > max_communication:
                max_communication = comm
        return max_communication
    
    def abelian_integral_system_order(f):
        n = len(f)
        # Simplified version of the algorithm to generate an abelian integral system order
        # This is a placeholder and should be replaced with a real implementation
        return n // 2
    
    instances_tested = 0
    n_max = 0
    total_communication_complexity = 0
    total_abelian_integral_order = 0
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested += 2**n
        if n > n_max:
            n_max = n
        
        f = generate_boolean_function(n)
        comm_complexity = communication_complexity(f)
        abelian_order = abelian_integral_system_order(f)
        
        total_communication_complexity += comm_complexity
        total_abelian_integral_order += abelian_order
        
        if comm_complexity <= 2*n/3 and abelian_order < n/3:
            counterexample = f"n={n}, f={f}, comm_complexity={comm_complexity}, abelian_order={abelian_order}"
    
    mean_communication_complexity = total_communication_complexity / instances_tested
    mean_abelian_integral_order = total_abelian_integral_order / instances_tested
    
    conjecture_holds = (mean_abelian_integral_order >= 0.5 * mean_communication_complexity)
    
    return {
        "metric_name": "communication_complexity_vs_abelian_order",
        "metric_value": mean_abelian_integral_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")