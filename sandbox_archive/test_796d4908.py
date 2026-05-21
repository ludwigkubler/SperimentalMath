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
    
    def hypergeometric_moment(n, k):
        if n <= 0 or k < 0:
            return 0
        return (math.comb(n, k) / math.factorial(k)) * (1 - (k / n))
    
    def ac0_circuit_size(depth):
        # Simplified model for AC0 circuit size based on depth
        return 2 ** depth
    
    def ac0_circuit_depth(size):
        # Simplified model for AC0 circuit depth based on size
        return math.log2(size)
    
    n_min = 5
    n_max = 40
    k_max = 10
    trials_per_n = 30
    
    total_moments = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.randint(n_min, n_max)
        d = ac0_circuit_depth(ac0_circuit_size(d))
        k = int(math.log2(n))
        
        if k > k_max:
            continue
        
        moments_sum = sum(hypergeometric_moment(n, i) for i in range(k + 1))
        size = ac0_circuit_size(d)
        ratio = moments_sum / (math.log(size) ** k)
        
        total_moments += moments_sum
        instances_tested += 1
        
        if not conjecture_holds and counterexample == "":
            continue
        
        if ratio < 0.5 * d or ratio > 2 * d:
            conjecture_holds = False
            counterexample = f"Circuit with n={n}, d={d} failed"
    
    mean_moments = total_moments / instances_tested if instances_tested > 0 else 0
    
    return {
        "metric_name": "Mean Moments Sum",
        "metric_value": mean_moments,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")