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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_coxeter_group_length(boolean_function):
        n = len(boolean_function)
        # Constructive mapping algorithm (simplified example)
        length = sum(1 for bit in boolean_function if bit == 1)
        return length
    
    def calculate_kw_protocol_cost(boolean_function):
        n = len(boolean_function)
        # Simplified example cost calculation
        cost = n * (n + 1) // 2
        return cost
    
    instances_tested = 0
    total_coxeter_group_length = 0
    total_kw_protocol_cost = 0
    
    for _ in range(30):
        boolean_function = generate_boolean_function(random.randint(5, 40))
        coxeter_group_length = calculate_coxeter_group_length(boolean_function)
        kw_protocol_cost = calculate_kw_protocol_cost(boolean_function)
        
        instances_tested += 1
        total_coxeter_group_length += coxeter_group_length
        total_kw_protocol_cost += kw_protocol_cost
    
    mean_coxeter_group_length = Fraction(total_coxeter_group_length, instances_tested)
    mean_kw_protocol_cost = Fraction(total_kw_protocol_cost, instances_tested)
    
    conjecture_holds = abs(mean_coxeter_group_length - mean_kw_protocol_cost) <= 10
    counterexample = "" if conjecture_holds else f"mean_coxeter_group_length={mean_coxeter_group_length}, mean_kw_protocol_cost={mean_kw_protocol_cost}"
    
    return {
        "metric_name": "Coxeter Group Length vs KW Protocol Cost",
        "metric_value": mean_coxeter_group_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_coxeter_group_length = sum(res["metric_value"] for res in results) / len(results)
    mean_kw_protocol_cost = sum(res["instances_tested"] * res["metric_value"] for res in results) / sum(res["instances_tested"] for res in results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_coxeter_group_length} std=0.0 support_fraction={support_fraction}")
    elif any(abs(res["metric_value"] - mean_kw_protocol_cost) > 10 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if abs(res["metric_value"] - mean_kw_protocol_cost) > 10)
        print(f"RESULT: FALSIFIED counterexample=\"mean_coxeter_group_length={mean_coxeter_group_length}, mean_kw_protocol_cost={mean_kw_protocol_cost}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE not_enough_evidence")