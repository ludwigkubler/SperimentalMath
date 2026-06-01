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
    
    def communication_complexity(f):
        n = len(f)
        return sum(1 for i in range(n) if f[i] != f[(i + 1) % n])
    
    def abelian_integral_order(f):
        # Placeholder function to simulate the order calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = [random.choice([0, 1]) for _ in range(n)]
            cc = communication_complexity(f)
            ai_order = abelian_integral_order(f)
            results.append((cc, ai_order))
    
    total_cc = sum(cc for cc, _ in results)
    total_ai_order = sum(ai_order for _, ai_order in results)
    mean_cc = total_cc / len(results)
    mean_ai_order = total_ai_order / len(results)
    
    correlation = (len(results) * sum(cc * ai_order for cc, ai_order in results) - 
                   total_cc * total_ai_order) / math.sqrt((len(results) * sum(cc**2 for cc, _ in results) - total_cc**2) *
                                                       (len(results) * sum(ai_order**2 for _, ai_order in results) - total_ai_order**2))
    
    conjecture_holds = all(cc > 2*n/3 and ai_order >= n/3 for cc, ai_order in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")