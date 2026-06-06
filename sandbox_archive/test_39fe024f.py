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
    
    def generate_random_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(n):
            clause = random.choice(variables + [f'~{var}' for var in variables])
            clauses.append(clause)
        return ' & '.join(clauses)
    
    def incidence_matrix(formula, n):
        matrix = [[0] * n for _ in range(2**n)]
        for i in range(2**n):
            assignment = [bool(i >> j & 1) for j in range(n)]
            if eval(formula, {'x': assignment}):
                for j in range(n):
                    if assignment[j]:
                        matrix[i][j] = 1
                    else:
                        matrix[i][j] = -1
        return matrix
    
    def min_order(matrix):
        p = 2  # Using base 2 for simplicity
        n = len(matrix)
        order = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                diff = sum(abs(a - b) for a, b in zip(matrix[i], matrix[j]))
                if diff < order:
                    order = diff
        return order
    
    def frege_proof_length(formula):
        # Placeholder function to simulate Frege proof length calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(formula.split(' & '))
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0.0
    max_n = -1
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            formula = generate_random_formula(n)
            matrix = incidence_matrix(formula, n)
            min_order_val = min_order(matrix)
            proof_length = frege_proof_length(formula)
            
            if min_order_val == 0 or proof_length == 0:
                continue
            
            metric_value = math.log(min_order_val) / math.log(2**proof_length + 1)
            total_metric_value += metric_value
            instances_tested += 1
            max_n = max(max_n, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "log(p-1)^min_order(Inc(φ)) vs log(2^{w(Frege(φ))) + 1)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "log(p-1)^min_order(Inc(φ)) vs log(2^{w(Frege(φ))) + 1)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    instances_tested = sum(r["instances_tested"] for r in results)
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] == "insufficient_instances" for r in results):
        print("RESULT: INCONCLUSIVE insufficient_instances")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[results.index(next((r for r in results if not r['conjecture_holds']), None))]}")