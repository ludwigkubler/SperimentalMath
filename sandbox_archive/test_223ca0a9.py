# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_representation(f, n):
        return [[[f[i * 2**(n-1) + j * 2**(n-2) + k] for k in range(2)] for j in range(2)] for i in range(2)]
    
    def geometric_entropy(tensor):
        total = sum(sum(sum(abs(x) for x in row) for row in layer) for layer in tensor)
        return -math.log(total, 2)
    
    def circuit_size(f, n):
        # Simple DPLL solver implementation
        def dpll(clauses, assignment):
            if not clauses:
                return True
            literal = next(lit for lit in range(-n, n+1) if lit not in assignment and -lit not in assignment)
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = value
                if dpll(clauses, new_assignment):
                    return True
            return False
        
        def cnf_to_clauses(cnf):
            return [[int(lit) for lit in clause.split()] for clause in cnf.split('\n') if clause]
        
        # Convert the Boolean function to CNF
        cnf = ""
        for i in range(2**n):
            binary = format(i, f'0{n}b')
            clause = []
            for j in range(n):
                if binary[j] == '1':
                    clause.append(j + 1)
                else:
                    clause.append(-(j + 1))
            cnf += " ".join(map(str, clause)) + "\n"
        
        clauses = cnf_to_clauses(cnf)
        return len(clauses) if dpll(clauses, {}) else float('inf')
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        tensor = tensor_representation(f, n)
        H_min = geometric_entropy(tensor)
        s_f = circuit_size(f, n)
        
        if s_f == float('inf'):
            continue
        
        results.append((H_min, math.log(s_f)))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "circuit_size_infinite"
        }
    
    H_min_avg = sum(H for H, _ in results) / len(results)
    log_s_f_avg = sum(log_s_f for _, log_s_f in results) / len(results)
    correlation_coefficient = (sum((H - H_min_avg) * (log_s_f - log_s_f_avg) for H, log_s_f in results) /
                               math.sqrt(sum((H - H_min_avg)**2 for H, _ in results) *
                                         sum((log_s_f - log_s_f_avg)**2 for _, log_s_f in results)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / sum(1 for result in results if result["conjecture_holds"])
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["conjecture_holds"])) / sum(1 for result in results if result["conjecture_holds"])
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")