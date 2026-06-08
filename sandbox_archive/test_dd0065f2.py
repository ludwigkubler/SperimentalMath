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
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            if all(f[j] == f[j + 2**i] for j in range(2**(n - i) - 1)):
                rank += 1
        return rank
    
    def eta_invariant(f):
        n = int(math.log2(len(f)))
        invariant = 0
        for i in range(n):
            for j in range(2**i):
                if f[j] != f[j + 2**i]:
                    invariant += 1
        return invariant / (n * 2**(n - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_eta = 0.0
    total_variance = 0.0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            eta = eta_invariant(f)
            variance = communication_complexity_rank_variance(f)
            total_eta += eta
            total_variance += variance
            instances_tested += 1
    
    mean_eta = total_eta / instances_tested
    mean_variance = total_variance / instances_tested
    correlation_coefficient = (instances_tested * sum(eta * variance for eta, variance in zip([mean_eta] * instances_tested, [mean_variance] * instances_tested)) -
                               instances_tested * mean_eta * mean_variance) / math.sqrt((instances_tested * sum(eta**2 for eta in [mean_eta] * instances_tested) - instances_tested * mean_eta**2) *
                                                                 (instances_tested * sum(variance**2 for variance in [mean_variance] * instances_tested) - instances_tested * mean_variance**2))
    
    return {
        "metric_name": "eta_variance_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")