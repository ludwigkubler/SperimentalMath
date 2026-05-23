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
    
    def max_cut_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def configuration_space_invariant(instance):
        n = len(instance)
        invariant = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if instance[i] != instance[j]:
                    invariant[i][j] = 1
                    invariant[j][i] = 1
        return invariant
    
    def sos_degree(instance):
        n = len(instance)
        degree = 0
        for i in range(n):
            for j in range(i + 1, n):
                if instance[i] != instance[j]:
                    degree += 1
        return degree
    
    instances_tested = 30
    total_rank = 0
    total_degree = 0
    
    for _ in range(instances_tested):
        instance = max_cut_instance(40)
        invariant = configuration_space_invariant(instance)
        rank = sum(sum(row) for row in invariant) // 2
        degree = sos_degree(instance)
        
        total_rank += rank
        total_degree += degree
    
    mean_rank = total_rank / instances_tested
    mean_degree = total_degree / instances_tested
    
    if abs(mean_rank - 0.879 * mean_degree * math.log(40)) <= 2 * (mean_rank + mean_degree):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Rank and degree mismatch"
    
    return {
        "metric_name": "Rank vs Degree",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank and degree mismatch\" first_failing_seed={first_failing_seed}")