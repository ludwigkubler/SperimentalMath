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

def generate_sat_instance(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def compute_min_order(clauses):
    n = len(clauses[0])
    min_order = 0
    for i in range(n):
        if all(any(j != k and abs(clause[i]) == abs(clause[k]) for clause in clauses) for j in range(i + 1, n)):
            min_order += 1
    return min_order

def compute_entropy(subset):
    n = len(subset)
    if n == 0:
        return 0.0
    p = Fraction(n, len(clauses))
    entropy = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n + 1, n * (n + 1) // 2)
        clauses = generate_sat_instance(n, m)
        
        subset_size = random.randint(1, len(clauses))
        subset = random.sample(clauses, subset_size)
        
        min_order = compute_min_order(clauses)
        entropy = compute_entropy(subset)
        
        metric_values.append((min_order, entropy))
    
    if not metric_values:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No data generated"
        }
    
    def rank(data):
        sorted_data = sorted([(x, i) for i, x in enumerate(data)])
        ranks = [0] * len(data)
        for i, (_, idx) in enumerate(sorted_data):
            ranks[idx] = i
        return ranks
    
    min_order_ranks = rank([x[0] for x in metric_values])
    entropy_ranks = rank([x[1] for x in metric_values])
    
    n = len(metric_values)
    spearman_corr = sum((min_order_ranks[i] - entropy_ranks[i]) ** 2 for i in range(n)) / (n * (n**2 - 1))
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": spearman_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": spearman_corr >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")