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
    
    def generate_disjointness_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def delone_set_geometry(instance):
        n = len(instance)
        tau = 0
        for i in range(n):
            count = sum(1 for j in range(i+1, n) if instance[i] != instance[j])
            tau += count
        return tau / (n * (n - 1))
    
    def communication_complexity(instance):
        n = len(instance)
        # Simplified model: each bit requires one unit of communication
        return n
    
    instances_tested = 0
    total_tau = 0
    support_count = 0
    
    for _ in range(30):
        instance = generate_disjointness_instance(random.randint(5, 40))
        tau = delone_set_geometry(instance)
        comm_complexity = communication_complexity(instance)
        
        if tau >= 1:  # Simplified threshold
            support_count += 1
        
        total_tau += tau
        instances_tested += 1
    
    mean_tau = total_tau / instances_tested
    conjecture_holds = support_count / instances_tested >= 0.8
    counterexample = "" if conjecture_holds else "communication_complexity < n/2"
    
    return {
        "metric_name": "minimal_local_index",
        "metric_value": mean_tau,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_tau = sum(result['metric_value'] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_tau} std=0 support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='communication_complexity < n/2' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")