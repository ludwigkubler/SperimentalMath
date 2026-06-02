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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n * (n - 1)):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses
    
    def circuit_weight(cnf):
        weight = 0
        for clause in cnf:
            weight += len(clause) + 1
        return weight
    
    def minimal_order_brauer_group(cnf):
        # Simplified mapping to avoid complex calculations
        n = len(cnf)
        if n == 1:
            return 2
        elif n == 2:
            return 3
        else:
            return n * (n + 1) // 2
    
    def log_brauer_group_order(order):
        return math.log(order, 10)
    
    instances_tested = 0
    total_log_order = 0
    total_weight = 0
    n_max = 1
    
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        weight = circuit_weight(cnf)
        order = minimal_order_brauer_group(cnf)
        log_order = log_brauer_group_order(order)
        
        instances_tested += 1
        total_log_order += log_order
        total_weight += weight
        n_max = max(n_max, n)
    
    mean_log_order = total_log_order / instances_tested
    mean_weight = total_weight / instances_tested
    
    correlation_coefficient = (instances_tested * sum(log_order * weight for log_order, weight in zip([math.log(order, 10) for order in [minimal_order_brauer_group(generate_cnf(n)) for n in range(5, 41)]], [circuit_weight(generate_cnf(n)) for n in range(5, 41)])) - mean_log_order * mean_weight) / (instances_tested * sum((log_order - mean_log_order) ** 2 for log_order in [math.log(order, 10) for order in [minimal_order_brauer_group(generate_cnf(n)) for n in range(5, 41)]]) - instances_tested * (mean_weight ** 2))
    
    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
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
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")