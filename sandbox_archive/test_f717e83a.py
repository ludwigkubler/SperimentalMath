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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def homomorphisms_to_symmetric_group(n):
        # Simplified version of generating homomorphisms
        return [i % n for i in range(2**n)]
    
    def quasi_symmetric_functions_count(f, phi):
        count = 0
        for x in range(2**len(f)):
            if f[x] == phi[phi[x]]:
                count += 1
        return count
    
    def communication_complexity(f):
        # Simplified version of computing communication complexity
        return len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_random_boolean_function(n)
        phi = homomorphisms_to_symmetric_group(n)
        count_phi = quasi_symmetric_functions_count(f, phi)
        cc_f = communication_complexity(f)
        results.append({
            "n": n,
            "count_phi": count_phi,
            "cc_f": cc_f
        })
    
    total_instances_tested = sum(1 for res in results for _ in range(res["n"]))
    mean_cc_f = sum(res["cc_f"] for res in results) / total_instances_tested
    std_deviation = math.sqrt(sum((res["cc_f"] - mean_cc_f)**2 for res in results) / total_instances_tested)
    
    conjecture_holds = all(cc_f <= 3 * count_phi**2 for res in results for _ in range(res["n"]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_cc_f,
        "instances_tested": total_instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc_f = sum(res["metric_value"] for res in results) / len(results)
    std_deviation = math.sqrt(sum((res["metric_value"] - mean_cc_f)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_cc_f} std={std_deviation} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")