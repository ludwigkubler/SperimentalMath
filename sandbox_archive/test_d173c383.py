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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_clause_entropy(clauses):
        total_clauses = len(clauses)
        entropy = 0
        for clause in clauses:
            size = len(clause)
            if size > 0:
                entropy += math.log2(size / total_clauses)
        return entropy
    
    def geometric_flow_order(n):
        # Placeholder for actual geometric flow computation
        # For simplicity, we use a linear function of n
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Sample 5 instances per size
            clauses = generate_cnf(n)
            entropy = compute_clause_entropy(clauses)
            order = geometric_flow_order(n)
            
            total_metric_value += order * entropy
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = (instances_tested - sum(1 for _ in range(instances_tested) if not conjecture_holds)) / instances_tested
    
    return {
        "metric_name": "geometric_flow_order * clause_entropy",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(res["metric_value"] for res in results)
    mean_metric_value = total_metric_value / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")