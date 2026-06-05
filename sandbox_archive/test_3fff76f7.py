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
        for _ in range(2**n):  # Generate all possible combinations of literals
            clause = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n+1)]
            if random.choice([True, False]):
                clause.append(random.choice([f'x{i}', f'-x{i}']))
            clauses.append(clause)
        return clauses
    
    def entropy(cnf):
        num_clauses = len(cnf)
        p = Fraction(num_clauses, 2**n)
        return -p * math.log2(p) + (1 - p) * math.log2(1 - p)
    
    def minimal_p_adic_valuation(x):
        if x == 0:
            return 0
        for i in range(1, abs(x) + 1):
            if x % i == 0 and all((x // i) % (j**p) != 0 for j in range(2, int(math.sqrt(abs(x))) + 1) for p in range(1, 5)):
                return i
        return abs(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different CNF formulas
            cnf = generate_cnf(n)
            entropy_value = entropy(cnf)
            val_p_entropy = minimal_p_adic_valuation(entropy_value)
            metric_values.append(val_p_entropy)
            instances_tested += 1
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = (sum((x - mean_metric_value)**2 for x in metric_values) / len(metric_values))**0.5
    correlation_coefficient = sum((i + n_values[0]) * (j - mean_metric_value) for i, j in enumerate(metric_values)) / (len(metric_values) * std_metric_value)
    
    conjecture_holds = correlation_coefficient > 0.95 and all(c >= 0.5 for c in metric_values)
    counterexample = "" if conjecture_holds else "correlation_too_low"
    
    return {
        "metric_name": "minimal_p_adic_valuation",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")