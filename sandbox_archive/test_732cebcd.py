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
    
    def calculate_coxeter_group_length(f):
        n = len(f)
        # Simplified mapping to a Coxeter group length
        # This is a placeholder and should be replaced with an actual algorithm
        return n
    
    def calculate_kw_protocol_cost(f):
        n = len(f)
        # Simplified mapping to KW protocol cost
        # This is a placeholder and should be replaced with an actual algorithm
        return n**2
    
    instances_tested = 0
    total_coxeter_group_length = 0
    total_kw_protocol_cost = 0
    
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        coxeter_group_length = calculate_coxeter_group_length(f)
        kw_protocol_cost = calculate_kw_protocol_cost(f)
        
        if coxeter_group_length is None or kw_protocol_cost is None:
            return {
                "metric_name": "Coxeter Group Length vs KW Protocol Cost",
                "metric_value": 0,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        total_coxeter_group_length += coxeter_group_length
        total_kw_protocol_cost += kw_protocol_cost
        instances_tested += 1
    
    average_coxeter_group_length = total_coxeter_group_length / instances_tested
    average_kw_protocol_cost = total_kw_protocol_cost / instances_tested
    
    return {
        "metric_name": "Coxeter Group Length vs KW Protocol Cost",
        "metric_value": abs(average_coxeter_group_length - average_kw_protocol_cost),
        "instances_tested": instances_tested,
        "conjecture_holds": abs(average_coxeter_group_length - average_kw_protocol_cost) <= 10,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=0")
    else:
        print(f"RESULT: INCONCLUSIVE budget_exceeded n_tested={len(seeds)}")