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
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def ideal_generated_by_variables(cnf):
        variables = set()
        for clause in cnf:
            for var in clause:
                variables.add(abs(var))
        return variables
    
    def minimal_local_ring_norm(ideal, n):
        if not ideal:
            return 0
        norm = len(ideal) ** (1/3) * math.log(n)
        return norm
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_dev_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_dev_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        if std_dev_x == 0 or std_dev_y == 0:
            return 0
        correlation = cov_xy / (std_dev_x * std_dev_y)
        return correlation
    
    n_values = [5, 10, 15, 20, 30, 40]
    local_ring_norms = []
    m_values = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = int(n ** (1/3) * math.log(n))
            cnf = generate_cnf(n, m)
            ideal = ideal_generated_by_variables(cnf)
            norm = minimal_local_ring_norm(ideal, n)
            local_ring_norms.append(norm)
            m_values.append(m)
    
    correlation_coefficient = pearson_correlation(local_ring_norms, m_values)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(local_ring_norms),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.9,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")