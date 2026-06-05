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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def entropy(cnf):
        total_clauses = len(cnf)
        if total_clauses == 0:
            return 0
        p = Fraction(total_clauses, total_clauses)
        return -p * math.log2(p) + (1 - p) * math.log2(1 - p)
    
    def minimal_p_adic_valuation(x):
        if x == 0:
            return 0
        for i in range(2, abs(x) + 1):
            if x % i == 0:
                return i
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_val_p_entropy = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # 5 instances per size
            cnf = generate_cnf(n, random.randint(1, n * 2))
            val_p_entropy = minimal_p_adic_valuation(entropy(cnf))
            total_val_p_entropy += val_p_entropy
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    mean_val_p_entropy = total_val_p_entropy / instances_tested
    conjecture_holds = False
    counterexample = ""
    
    # Linear regression to check correlation
    x_values = list(range(5, 41))
    y_values = [mean_val_p_entropy] * len(x_values)
    n_samples = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_xx = sum(x ** 2 for x in x_values)
    
    slope = (n_samples * sum_xy - sum_x * sum_y) / (n_samples * sum_xx - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n_samples
    
    correlation_coefficient = (n_samples * sum_xy - sum_x * sum_y) / math.sqrt((n_samples * sum_xx - sum_x ** 2) * (n_samples * sum_yy - sum_y ** 2))
    
    if correlation_coefficient > 0.95:
        conjecture_holds = True
    
    return {
        "metric_name": "minimal_p_adic_valuation_of_entropy",
        "metric_value": mean_val_p_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")