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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def entropy(clauses):
        total_clauses = len(clauses)
        count_dict = {}
        for clause in clauses:
            key = tuple(sorted(abs(x) for x in clause))
            if key not in count_dict:
                count_dict[key] = 0
            count_dict[key] += 1
        entropy = 0.0
        for count in count_dict.values():
            p = count / total_clauses
            entropy -= p * math.log2(p)
        return entropy
    
    def minimal_index(clauses):
        n = len(clauses[0])
        max_value = 0
        for i in range(1 << n):
            assignment = [(-1) ** (i >> j & 1) for j in range(n)]
            value = sum(abs(x * a) for x, a in zip(clauses[0], assignment))
            if value > max_value:
                max_value = value
        return max_value
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        entropy_val = entropy(cnf)
        index_val = minimal_index(cnf)
        results.append((n, entropy_val, index_val))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    entropy_vals = [r[1] for r in results]
    index_vals = [r[2] for r in results]
    
    mean_entropy = sum(entropy_vals) / len(entropy_vals)
    mean_index = sum(index_vals) / len(index_vals)
    
    covariance = sum((e - mean_entropy) * (i - mean_index) for e, i in zip(entropy_vals, index_vals)) / len(entropy_vals)
    variance_entropy = sum((e - mean_entropy) ** 2 for e in entropy_vals) / len(entropy_vals)
    variance_index = sum((i - mean_index) ** 2 for i in index_vals) / len(index_vals)
    
    pearson_corr = covariance / math.sqrt(variance_entropy * variance_index)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": pearson_corr > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i, r) for i, r in enumerate(results) if r["metric_value"] is None)[0]
        counterexample = "not_enough_instances"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")