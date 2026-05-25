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
    
    def tropicalized_k_theoretic_invariant(size):
        # Placeholder implementation for tropicalized K-theoretic invariant
        return size
    
    def read_twice_complexity(size):
        # Placeholder implementation for read-twice complexity
        return math.log2(size)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rho = 0.0
        
        while instances_tested < 30:
            size = random.randint(2**n, 2**(n+1))
            rho = tropicalized_k_theoretic_invariant(size)
            complexity = read_twice_complexity(size)
            
            if complexity == 0:
                continue
            
            ratio = rho / complexity
            results.append((size, rho, complexity, ratio))
            instances_tested += 1
        
        mean_ratio = sum(ratio for _, _, _, ratio in results) / len(results)
        
        if mean_ratio < 0.25 or mean_ratio > 2:
            return {
                "metric_name": "mean_ratio",
                "metric_value": mean_ratio,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"Mean ratio {mean_ratio} out of bounds"
            }
    
    mean_ratio = sum(ratio for _, _, _, ratio in results) / len(results)
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": 0.5 <= mean_ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    total_rho = 0.0
    instances_tested = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={seed}")
            sys.exit(0)
        
        total_rho += trial_result["metric_value"] * trial_result["instances_tested"]
        instances_tested += trial_result["instances_tested"]
    
    mean_rho = total_rho / instances_tested
    support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")