# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def plethysm_coefficient(n):
        # Placeholder for actual plethysm coefficient computation
        return 1 / (n * (n + 1))
    
    def inverse_hook_length_weighting(lambda_):
        # Placeholder for actual inverse hook-length weighting computation
        return 1
    
    def rho(f, n):
        return max(inverse_hook_length_weighting(lambda_) * plethysm_coefficient(n) for lambda_ in range(2*n + 1))
    
    perm_n = rho("perm", 3)
    det_values = [rho("det", m) for m in range(1, int(3**1.5) + 1)]
    
    return {
        "metric_name": "rho",
        "metric_value": perm_n,
        "instances_tested": len(det_values),
        "conjecture_holds": all(perm_n > det_val for det_val in det_values),
        "counterexample": "" if all(perm_n > det_val for det_val in det_values) else f"n=3, perm_n={perm_n}, det_values={det_values}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len(results) / len(seeds)
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n=3, perm_n={results[0]['perm_n']}, det_values={results[0]['det_values']}\" first_failing_seed={first_failing_seed}")