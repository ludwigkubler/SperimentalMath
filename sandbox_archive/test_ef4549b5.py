# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_regex(n):
        if n == 0:
            return 'ε'
        elif n == 1:
            return 'a|b'
        else:
            return '(' + generate_regex(random.randint(0, n-1)) + ')(' + generate_regex(random.randint(0, n-1)) + ')'

    def is_equivalent(s1, s2):
        if len(s1) != len(s2):
            return False
        for a in 'ab':
            if not all(s1.replace('a', a).replace('b', b) == s2.replace('a', a).replace('b', b) for b in 'ab'):
                return False
        return True

    def automorphism_group(regex):
        n = regex.count('a') + regex.count('b')
        if n == 0:
            return set()
        aut_group = set()
        for perm in itertools.permutations('ab' * (n // 2)):
            permuted_regex = ''.join(perm[i] for i in range(n))
            if is_equivalent(regex, permuted_regex):
                aut_group.add(perm)
        return aut_group

    def frege_proof_depth(regex):
        # Placeholder function to simulate Frege proof depth calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(regex)

    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            regex = generate_regex(n)
            aut_group = automorphism_group(regex)
            d_Frege = frege_proof_depth(regex)
            
            metric_values.append(len(aut_group))
            instances_tested += 1
    
    if len(metric_values) < 30:
        return {
            "metric_name": "AutGroupRank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    
    correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(metric_values, [frege_proof_depth(generate_regex(n)) for n in [5, 10, 15, 20, 30, 40]])) / len(metric_values)
    
    return {
        "metric_name": "AutGroupRank",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7 and correlation_coefficient < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")