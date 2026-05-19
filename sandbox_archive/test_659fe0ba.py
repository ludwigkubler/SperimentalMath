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
    
    n = 10  # Start with a small size and increase if needed
    
    while True:
        P = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        
        # Check if the transition matrix is valid
        if all(all(P[i][j] == P[j][i] for j in range(i+1, n)) for i in range(n)):
            break
    
    # Compute the free entropy ϕ(P)
    def log_moment_generating_function(matrix):
        n = len(matrix)
        moment = 0
        for k in range(1, n + 1):
            sum_k = 0
            for i in range(k):
                for j in range(k):
                    if i != j:
                        sum_k += matrix[i][j] * matrix[j][i]
            moment += math.log((n - k) / (k * (n - k))) * sum_k
        return moment
    
    ϕ_P = log_moment_generating_function(P)
    
    # Check the size condition and the free entropy threshold
    size_condition = 2 ** n // 2 <= len(P)
    free_entropy_threshold = math.log(n) ** 2
    
    result = {
        "metric_name": "free_entropy",
        "metric_value": ϕ_P,
        "instances_tested": 1,
        "conjecture_holds": size_condition and ϕ_P >= free_entropy_threshold,
        "counterexample": "" if size_condition and ϕ_P >= free_entropy_threshold else f"Size: {len(P)}, Free Entropy: {ϕ_P}"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    total_metric_value = 0.0
    support_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            support_count += 1
        
        results.append(trial_result)
    
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = support_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Size condition or free entropy threshold not met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")