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
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
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
    counts = [0] * len(subset)
    for clause in subset:
        for var in clause:
            if var > 0:
                counts[var - 1] += 1
            else:
                counts[-var - 1] -= 1
    total = sum(abs(count) for count in counts)
    entropy = 0.0
    for count in counts:
        if count != 0:
            p = Fraction(abs(count), total)
            entropy -= p * math.log2(p)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    min_order_sum = 0.0
    entropy_sum = 0.0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_sat_instance(n, random.randint(1, n * (n + 1) // 2))
            subset_size = random.randint(1, len(clauses))
            subset = random.sample(clauses, subset_size)
            
            min_order = compute_min_order(subset)
            entropy = compute_entropy(subset)
            
            min_order_sum += min_order
            entropy_sum += entropy
            instances_tested += 1
    
    mean_min_order = min_order_sum / instances_tested
    mean_entropy = entropy_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(min_order * entropy for min_order, entropy in zip(range(instances_tested), range(instances_tested))) - 
                               mean_min_order * mean_entropy) / math.sqrt((instances_tested * sum(min_order ** 2 for min_order in range(instances_tested)) - mean_min_order ** 2) *
                                                                        (instances_tested * sum(entropy ** 2 for entropy in range(instances_tested)) - mean_entropy ** 2))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "Spearman's rank correlation coefficient < 0.7"
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")