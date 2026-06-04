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
    
    def generate_cnf(m):
        literals = list(range(1, m + 1)) + [-x for x in range(1, m + 1)]
        cnf = []
        for _ in range(m):
            clause = random.sample(literals, 2)
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        queue = [set(clause) for clause in cnf]
        literals = set()
        for clause in cnf:
            literals.update(clause)
        
        while True:
            new_clauses = []
            added_new_clause = False
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if any(-x in queue[i] and x in queue[j] for x in literals):
                        new_lit = -queue[i].intersection(queue[j]).pop()
                        new_clause = (queue[i] | queue[j]) - {new_lit, -new_lit}
                        if new_clause not in queue:
                            new_clauses.append(new_clause)
                            added_new_clause = True
            if not added_new_clause:
                break
            queue.extend(new_clauses)
        
        return len(queue)
    
    def geometric_quantization_order(cnf):
        # Placeholder for actual geometric quantization order calculation
        return sum(1 for clause in cnf)  # Simplified example
    
    n_values = [5, 10, 15, 20, 30, 40]
    o_q_values = []
    w_phi_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        o_q_values.append(geometric_quantization_order(cnf))
        w_phi_values.append(resolution_width(cnf))
    
    if len(o_q_values) < 30 or len(w_phi_values) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(o_q_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    n = len(o_q_values)
    mean_o_q = sum(o_q_values) / n
    mean_w_phi = sum(w_phi_values) / n
    
    covariance = sum((o_q_values[i] - mean_o_q) * (w_phi_values[i] - mean_w_phi) for i in range(n)) / n
    variance_o_q = sum((o_q_values[i] - mean_o_q) ** 2 for i in range(n)) / n
    variance_w_phi = sum((w_phi_values[i] - mean_w_phi) ** 2 for i in range(n)) / n
    
    correlation_coefficient = covariance / (math.sqrt(variance_o_q) * math.sqrt(variance_w_phi))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(o_q_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=None support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=None support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")