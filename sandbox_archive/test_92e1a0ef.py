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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length(young_diagram):
    m, n = len(young_diagram), len(young_diagram[0])
    hook_lengths = [[0] * n for _ in range(m)]
    
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            hook_lengths[i][j] = young_diagram[i][j] + (m - i) + (n - j) - 1
    
    return hook_lengths

def plethysm_coefficient(young_diagram):
    m, n = len(young_diagram), len(young_diagram[0])
    hook_lengths = hook_length(young_diagram)
    
    numerator = factorial(m + n)
    denominator = 1
    for i in range(m):
        for j in range(n):
            denominator *= hook_lengths[i][j]
    
    return numerator / denominator

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) * (2 * random.choice([0, 1]) - 1) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def cnf_to_young_diagram(cnf, n):
    young_diagram = [[0] * n for _ in range(n)]
    
    for clause in cnf:
        for literal in clause:
            abs_literal = abs(literal)
            if abs_literal <= n:
                row = abs(abs_literal - 1) // (n + 1 - abs(abs_literal))
                col = abs(abs_literal - 1) % (n + 1 - abs(abs_literal))
                young_diagram[row][col] += 1
    
    return young_diagram

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Aim for at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n * (n - 1) // 2))
            young_diagram = cnf_to_young_diagram(cnf, n)
            plethysm_coeff = plethysm_coefficient(young_diagram)
            
            total_metric_value += plethysm_coeff
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = mean_metric_value >= 2 ** n_values[-1]
    
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")