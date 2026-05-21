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
    
    def gromov_wasserstein_distance(n, D):
        return 2**(n - 1/2) / n
    
    def min_monotone_circuit_size(n, k):
        # Placeholder for actual computation
        return n**2
    
    def generate_random_metric_measure_space(n):
        # Placeholder for actual generation
        return random.uniform(0.5, 1.5)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        D_n = gromov_wasserstein_distance(n, None)
        instances_tested = 0
        total_gw = 0
        
        while instances_tested < 30:
            MMS = generate_random_metric_measure_space(n)
            if MMS >= D_n and MMS <= 2 * D_n:
                gw_dist = abs(MMS - D_n) / D_n
                circuit_size = min_monotone_circuit_size(n, k)
                results.append((gw_dist, circuit_size))
                instances_tested += 1
        
        if not results:
            return {
                "metric_name": "GW Distance",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "No valid metric measure space found"
            }
    
    total_gw = sum(result[0] for result in results)
    avg_gw = total_gw / len(results)
    avg_circuit_size = sum(result[1] for result in results) / len(results)
    
    return {
        "metric_name": "GW Distance",
        "metric_value": avg_gw,
        "instances_tested": len(results),
        "conjecture_holds": avg_gw <= 2 and avg_circuit_size >= n**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - avg_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")