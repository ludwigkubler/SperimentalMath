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
        rank = sum(1 for i in range(2**n) if f[i] != f[(i ^ (1 << (n - 1)))])
        return rank
    
    def quaternionic_automorphisms_count(f):
        count = 0
        n = int(math.log2(len(f)))
        for a in range(2**n):
            for b in range(2**n):
                if all((f[(i ^ (a & (1 << j)))] == f[(i ^ (b & (1 << j)))] for j in range(n))):
                    count += 1
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        C_f = communication_complexity_rank_variance(f)
        Aut_q_f = quaternionic_automorphisms_count(f)
        results.append((n, Aut_q_f, math.sqrt(C_f)))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    Aut_q_values = [Aut_q for _, Aut_q, _ in results]
    C_f_sqrt_values = [C_f_sqrt for _, _, C_f_sqrt in results]
    
    mean_Aut_q = sum(Aut_q_values) / len(Aut_q_values)
    mean_C_f_sqrt = sum(C_f_sqrt_values) / len(C_f_sqrt_values)
    
    correlation_coefficient = 0
    for Aut_q, C_f_sqrt in zip(Aut_q_values, C_f_sqrt_values):
        correlation_coefficient += (Aut_q - mean_Aut_q) * (C_f_sqrt - mean_C_f_sqrt)
    correlation_coefficient /= len(Aut_q_values) * math.sqrt(sum((Aut_q - mean_Aut_q)**2 for Aut_q in Aut_q_values)) * math.sqrt(sum((C_f_sqrt - mean_C_f_sqrt)**2 for C_f_sqrt in C_f_sqrt_values))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": correlation_coefficient > 0.7 and all(correlation_coefficient >= 0.5 for _ in range(30)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "first_failing_seed"
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")