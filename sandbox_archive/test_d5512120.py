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
    
    def is_monotone(f):
        for i in range(2**len(f)):
            x = [bool(i >> j & 1) for j in range(len(f))]
            if f(x[0]) < f(x[1]):
                return False
        return True
    
    def generate_quandle_representations(n):
        quandles = []
        for i in range(2**n):
            quandle = {}
            for j in range(2**n):
                quandle[(i, j)] = random.randint(0, n-1)
            quandles.append(quandle)
        return quandles
    
    def min_rank(quandle):
        # Compute the minimal rank of a quandle representation
        # This is a placeholder implementation; actual computation depends on the specific structure of the quandle
        return 1  # Placeholder value
    
    c_Q = 1.0  # Placeholder constant for demonstration purposes
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        min_rank_total = 0
        
        for _ in range(5):  # Test each n with 5 instances
            f = lambda x: random.choice([x[0], not x[0]]) if len(x) == 1 else random.choice([f(x[:-1]), not f(x[:-1])])
            quandles = generate_quandle_representations(n)
            
            for quandle in quandles:
                if is_monotone(f):
                    min_rank_value = min_rank(quandle)
                    min_rank_total += min_rank_value
                    instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "min_rank",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "No monotone boolean functions found"
            }
        
        avg_min_rank = min_rank_total / instances_tested
        results.append(avg_min_rank)
    
    support_fraction = sum(r >= c_Q * math.log(n) for n, r in zip(n_values, results)) / len(n_values)
    
    if support_fraction == 1.0:
        return {
            "metric_name": "min_rank",
            "metric_value": sum(results) / len(results),
            "instances_tested": instances_tested * len(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        first_failing_seed = seed
        for n, r in zip(n_values, results):
            if r < c_Q * math.log(n):
                first_failing_seed = seed
                break
        
        return {
            "metric_name": "min_rank",
            "metric_value": sum(results) / len(results),
            "instances_tested": instances_tested * len(n_values),
            "conjecture_holds": False,
            "counterexample": f"First failing seed: {first_failing_seed}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if all(r is not None for r in results):
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if r >= c_Q * math.log(n_values[i])) / len(results)
        
        if support_fraction == 1.0:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(min(r for r in results if r < c_Q * math.log(n_values[i])))]
            print(f"RESULT: FALSIFIED counterexample='First failing seed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some trials had no monotone boolean functions")