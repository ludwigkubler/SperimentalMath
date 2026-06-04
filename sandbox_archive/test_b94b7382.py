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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll(instance):
        n = len(instance)
        assignment = [-1] * n
        stack = []
        
        def backtrack(i):
            if i == n:
                return True
            if instance[i] != -1:
                return backtrack(i + 1)
            
            for val in [0, 1]:
                assignment[i] = val
                if all(instance[j] == (assignment[j] if j < i else -1) for j in range(n)):
                    stack.append((i, val))
                    if backtrack(i + 1):
                        return True
                    stack.pop()
            assignment[i] = -1
            return False
        
        return backtrack(0)
    
    def monomial_generators(instance):
        n = len(instance)
        generators = set()
        
        def is_monomial(var, value):
            return all(instance[var] == (value if i == var else -1) for i in range(n))
        
        for i in range(n):
            if instance[i] != -1:
                continue
            for val in [0, 1]:
                if is_monomial(i, val):
                    generators.add((i, val))
        
        return len(generators)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            instance = generate_boolean_instance(n)
            dpll_length = len(dpll(instance))
            num_generators = monomial_generators(instance)
            
            if dpll_length == 0 or num_generators == 0:
                continue
            
            instances_tested += 1
            n_max = max(n_max, n)
            metrics.append((num_generators, dpll_length))
    
    if not metrics:
        return {
            "metric_name": "monomial_generators_vs_dpll",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    num_generators = [m[0] for m in metrics]
    dpll_lengths = [m[1] for m in metrics]
    correlation_coefficient = sum((num_generators[i] - mean_num) * (dpll_lengths[i] - mean_dPLL) for i in range(len(metrics))) / len(metrics)
    mean_num = sum(num_generators) / len(num_generators)
    mean_dPLL = sum(dpll_lengths) / len(dPLL_lengths)
    
    return {
        "metric_name": "monomial_generators_vs_dpll",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient=0' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")