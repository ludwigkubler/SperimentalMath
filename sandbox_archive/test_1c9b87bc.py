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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(random.randint(1, n * (n - 1) // 2)):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def compute_entropy(clauses):
        counts = {}
        for clause in clauses:
            key = tuple(sorted(clause))
            counts[key] = counts.get(key, 0) + 1
        entropy = 0.0
        total_clauses = len(clauses)
        for count in counts.values():
            p = count / total_clauses
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    def compute_min_order(clauses):
        n = len(set(abs(lit) for clause in clauses for lit in clause))
        order = 1
        while True:
            found = False
            for i in range(n):
                if all(any(j != k and abs(clause[i]) == abs(clause[k]) for clause in clauses) for j in range(i + 1, n)):
                    found = True
                    break
            if not found:
                return order
            order += 1
    
    n_max = 40
    instances_tested = 0
    min_order_values = []
    entropy_values = []
    
    for _ in range(30):
        n = random.randint(5, n_max)
        clauses = generate_sat_instance(n)
        min_order = compute_min_order(clauses)
        entropy = compute_entropy(clauses)
        
        min_order_values.append(min_order)
        entropy_values.append(entropy)
        instances_tested += 1
    
    correlation_coefficient = sum((min_order_values[i] - sum(min_order_values) / len(min_order_values)) * 
                                   (entropy_values[i] - sum(entropy_values) / len(entropy_values)) for i in range(len(min_order_values))) / \
                              (len(min_order_values) * math.sqrt(sum((x - sum(min_order_values) / len(min_order_values)) ** 2 for x in min_order_values)) *
                               math.sqrt(sum((y - sum(entropy_values) / len(entropy_values)) ** 2 for y in entropy_values)))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")