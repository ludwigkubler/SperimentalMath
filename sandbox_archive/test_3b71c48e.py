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
    
    def morse_function(f):
        n = int(math.log2(len(f)))
        morse_f = []
        for i in range(2**n):
            count_0 = f[i].count(0)
            count_1 = f[i].count(1)
            if count_0 == 0 or count_1 == 0:
                morse_f.append(0)
            else:
                morse_f.append(count_1 / (count_0 + count_1))
        return morse_f
    
    def topological_entropy(h):
        h = [x for x in h if x != 0]
        return sum(x * math.log2(1 / x) for x in h)
    
    def communication_rank(morse_f):
        n = int(math.log2(len(morse_f)))
        rank = 0
        for i in range(n):
            count_0 = morse_f[i].count(0)
            count_1 = morse_f[i].count(1)
            if count_0 == 0 or count_1 == 0:
                continue
            rank += max(count_0, count_1)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        morse_f = morse_function(f)
        h_morse_f = topological_entropy(morse_f)
        r_f = communication_rank(morse_f)
        results.append((n, h_morse_f, r_f))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n_max = max(n for n, _, _ in results)
    instances_tested = len(results)
    
    correlation_coefficients = []
    for i in range(instances_tested):
        for j in range(i + 1, instances_tested):
            h_i, r_i = results[i][1], results[j][2]
            h_j, r_j = results[j][1], results[i][2]
            numerator = (h_i - h_j) * (r_i - r_j)
            denominator = math.sqrt((h_i**2 + h_j**2) * (r_i**2 + r_j**2))
            if denominator == 0:
                correlation_coefficients.append(0)
            else:
                correlation_coefficients.append(numerator / denominator)
    
    mean_corr = sum(correlation_coefficients) / len(correlation_coefficients)
    std_corr = math.sqrt(sum((x - mean_corr)**2 for x in correlation_coefficients) / len(correlation_coefficients))
    
    conjecture_holds = all(abs(corr - 1) <= 2**n_max/3 for n, h_morse_f, r_f in results)
    counterexample = "" if conjecture_holds else "correlation_outside_bound"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")