# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        num_clauses = 2 * n
        literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
        cnf = []
        for _ in range(num_clauses):
            clause = random.sample(literals, 3)
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        seen = set()
        queue = [set(clause) for clause in cnf]
        while queue:
            new_queue = []
            for clause1 in queue:
                for clause2 in queue:
                    if len(clause1 & clause2) == 1:
                        lit = next(lit for lit in clause1 if lit > 0 and -lit not in seen)
                        new_clause = (clause1 | clause2) - {lit, -lit}
                        if new_clause:
                            if new_clause in seen:
                                continue
                            seen.add(new_clause)
                            new_queue.append(new_clause)
            queue = new_queue
        return len(seen)

    def minimal_index_of_algebraic_coadjointness(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        vector_space = [tuple([0] * (n + 1)) for _ in range(2 ** n)]
        
        def apply_operator(operator, vector):
            result = [0] * (n + 1)
            for i in range(n + 1):
                if operator[i]:
                    result[i] += vector[i]
            return tuple(result)
        
        operators = []
        for _ in range(2 ** n):
            operator = [random.choice([0, 1]) for _ in range(n + 1)]
            operators.append(operator)
        
        max_index = 0
        for i in range(len(operators)):
            for j in range(i + 1, len(operators)):
                index = sum(operators[i][k] * operators[j][k] for k in range(n + 1))
                max_index = max(max_index, abs(index))
        
        return max_index
    
    n_values = [5, 10, 15, 20, 30, 40]
    all_results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        algebraic_index = minimal_index_of_algebraic_coadjointness(cnf)
        proof_width = resolution_width(cnf)
        all_results.append((algebraic_index, proof_width))
    
    if not all_results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    algebraic_indices = [result[0] for result in all_results]
    proof_widths = [result[1] for result in all_results]
    
    mean_algebraic_index = sum(algebraic_indices) / len(algebraic_indices)
    mean_proof_width = sum(proof_widths) / len(proof_widths)
    
    correlation_coefficient = sum((algebraic_indices[i] - mean_algebraic_index) * (proof_widths[i] - mean_proof_width) for i in range(len(all_results))) / len(all_results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(all_results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE all_trials_used_n=1")