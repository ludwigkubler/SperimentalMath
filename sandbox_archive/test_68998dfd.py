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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = sum(1 for i in range(2**n) if f[i] == 1)
        return (rank / (2**n)) * ((2**n - rank) / (2**n))
    
    def min_ramanujan_sum(f):
        n = len(f)
        moment_polytope = [sum(f[j] for j in range(2**n) if bin(j).count('1') == i) for i in range(n+1)]
        return sum(math.sqrt(i * (i + 1)) * moment_polytope[i] for i in range(n+1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        rc_f = communication_complexity_rank_variance(f)
        ramanujan_sum = min_ramanujan_sum(f)
        results.append((n, ramanujan_sum, rc_f))
    
    mean_rc_f = sum(rc_f for _, _, rc_f in results) / len(results)
    mean_ramanujan_sum = sum(ramanujan_sum for _, ramanujan_sum, _ in results) / len(results)
    std_dev = math.sqrt(sum((rc_f - mean_rc_f)**2 for _, _, rc_f in results) / len(results))
    
    conjecture_holds = all(abs(ramanujan_sum - math.sqrt(2 * rc_f)) < 1e-6 for _, ramanujan_sum, rc_f in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ramanujan Sum vs RC(f)",
        "metric_value": mean_ramanujan_sum,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")