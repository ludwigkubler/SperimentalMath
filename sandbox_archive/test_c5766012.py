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
    
    def compute_nonlinearity(f):
        n = int(math.log2(len(f)))
        max_linear_approximation_error = sum(abs(sum(f[i:i+n] for i in range(j, len(f), n)) - f[j]) for j in range(n))
        return n - max_linear_approximation_error
    
    def compute_coxeter_group_action(f):
        n = int(math.log2(len(f)))
        transpositions = set()
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    transpositions.add((i, j))
        return len(transpositions)
    
    def inverse_ackermann(n):
        a = 0
        while n >= 2:
            n = math.ceil(math.log(n, 2))
            a += 1
        return a
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_transpositions = 0
    nonlinearity_sum = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            transpositions = compute_coxeter_group_action(f)
            nonlinearity = compute_nonlinearity(f)
            
            if transpositions > 2**n / (nonlinearity ** 0.5):
                return {
                    "metric_name": "Transpositions",
                    "metric_value": transpositions,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"Nonlinearity {nonlinearity} too low for {n} variables"
                }
            
            total_transpositions += transpositions
            nonlinearity_sum += nonlinearity
            instances_tested += 1
    
    mean_transpositions = total_transpositions / instances_tested
    avg_nonlinearity = nonlinearity_sum / instances_tested
    
    if any(transpositions >= 2**n * inverse_ackermann(n) for n in n_values):
        return {
            "metric_name": "Transpositions",
            "metric_value": mean_transpositions,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": f"Nonlinearity too low for some n"
        }
    
    return {
        "metric_name": "Transpositions",
        "metric_value": mean_transpositions,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Nonlinearity too low for some n\" first_failing_seed={r['seed']}")
                break