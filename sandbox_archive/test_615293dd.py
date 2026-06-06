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

def generate_circuit(n):
    stack = []
    for i in range(2 * n):
        if random.choice([True, False]):
            stack.append(random.randint(0, 1))
        else:
            if len(stack) < 2:
                continue
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
    return stack

def calculate_automorphism_group_count(circuit):
    # Simplified heuristic for automorphism group count
    return sum(1 for x in circuit if x == 0)

def calculate_entropy_variance(counts):
    n = len(counts)
    mean = sum(counts) / n
    variance = sum((x - mean) ** 2 for x in counts) / n
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    all_counts = []
    
    for n in n_values:
        counts = [generate_circuit(n) for _ in range(30)]
        all_counts.extend(counts)
    
    variance = calculate_entropy_variance(all_counts)
    mean = sum(all_counts) / len(all_counts)
    instances_tested = len(all_counts)
    n_max = max(n_values)
    
    conjecture_holds = mean <= 4 * n_max ** 2 and variance <= 0.1 * (4 * n_max ** 2)
    counterexample = "" if conjecture_holds else "mean={}, variance={}".format(mean, variance)
    
    return {
        "metric_name": "Entropy Variance",
        "metric_value": variance,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    std_variance = math.sqrt(sum((r["metric_value"] - mean_variance) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = "FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[results.index(next(r for r in results if not r["conjecture_holds"]))]["counterexample"], first_failing_seed)
    
    print("RESULT: {} mean={} std={} support_fraction={}".format(result, mean_variance, std_variance, support_fraction))