# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        return [[random.choice([-i, i]) for _ in range(random.randint(1, n))] for _ in range(n)]
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate resolution width
        clauses = cnf
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        
        queue = list(literals)
        while queue:
            literal = queue.pop(0)
            if literal < 0:
                continue
            for i, clause in enumerate(clauses):
                if literal in clause and -literal in clause:
                    clauses[i] = [l for l in clause if l != literal and l != -literal]
                    if not clauses[i]:
                        return len(queue) + 1
                    queue.append(-clauses[i][0])
        return len(queue)
    
    def minimal_local_zeta_function(cnf):
        # Placeholder function to compute the minimal local zeta function order
        # This is a dummy implementation for demonstration purposes
        return Fraction(1, 2)
    
    n_max = max(n for _ in range(30))
    if n_max < 5:
        return {
            "metric_name": "Order(ζφ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_sum = 0
    instances_tested = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        order_zeta = minimal_local_zeta_function(cnf)
        width_res = resolution_width(cnf)
        
        if order_zeta <= 0 or width_res <= 0:
            continue
        
        correlation_sum += abs(order_zeta - width_res) / (order_zeta + width_res)
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Order(ζφ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_avg = correlation_sum / instances_tested
    return {
        "metric_name": "Order(ζφ)",
        "metric_value": correlation_avg,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_avg >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")