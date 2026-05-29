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
    
    def generate_random_graph(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        if n == 0:
            return [1]
        elif n == 1:
            return [matrix[0][0] - 1, 1]
        
        det = 0
        for j in range(n):
            sub_matrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += ((-1) ** j) * matrix[0][j] * characteristic_polynomial(sub_matrix)
        return [det]
    
    def free_entropy(matrix):
        n = len(matrix)
        coeffs = characteristic_polynomial(matrix)
        total = sum(coeffs)
        entropy = 0
        for coeff in coeffs:
            if coeff > 0:
                p = coeff / total
                entropy -= p * math.log2(p)
        return entropy
    
    def communication_complexity(n):
        # Placeholder function; replace with actual computation
        return random.random() * n
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_cc_disj_n = 0.0
    total_h_f = 0.0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            graph = generate_random_graph(n)
            h_f = free_entropy(graph)
            cc_disj_n = communication_complexity(n)
            
            if h_f > 0:
                total_cc_disj_n += cc_disj_n
                total_h_f += h_f
                instances_tested += 1
    
    mean_cc_disj_n = total_cc_disj_n / instances_tested
    mean_h_f = total_h_f / instances_tested
    
    if instances_tested < 30:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    c = mean_cc_disj_n / math.log2(mean_h_f)
    conjecture_holds = all(cc_disj_n >= c * math.log2(h_f) for h_f, cc_disj_n in zip(total_h_f, total_cc_disj_n))
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_cc_disj_n,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"c={c}, {mean_cc_disj_n} < {c * math.log2(mean_h_f)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"c={results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")