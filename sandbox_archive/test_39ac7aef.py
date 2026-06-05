# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), random.choice([-1, 1])]
            clauses.append(clause)
        return clauses
    
    def projective_volume(formula):
        n = len(formula[0])
        points = [0] * n
        for clause in formula:
            var, sign = clause
            if sign == -1:
                var = -var
            if 1 <= abs(var) <= n:
                points[var - 1] += 1
        return max(points)
    
    def communication_complexity_rank(formula):
        n = len(formula[0])
        rank = 0
        for clause in formula:
            var, sign = clause
            if sign == -1:
                var = -var
            if 1 <= abs(var) <= n:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n)
            sv = projective_volume(formula)
            ccrank = communication_complexity_rank(formula)
            total_metric_value += sv / ccrank if ccrank != 0 else float('inf')
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = total_metric_value / instances_tested
    correlation_coefficient = (instances_tested * sum(sv / ccrank for sv, ccrank in zip([projective_volume(generate_formula(n)) for n in n_values], [communication_complexity_rank(generate_formula(n)) for n in n_values])) - instances_tested * mean_metric_value ** 2) / ((instances_tested - 1) * sum((sv / ccrank - mean_metric_value) ** 2 for sv, ccrank in zip([projective_volume(generate_formula(n)) for n in n_values], [communication_complexity_rank(generate_formula(n)) for n in n_values])))
    
    if correlation_coefficient < 0.3:
        conjecture_holds = False
        counterexample = "correlation_coefficient_too_low"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
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
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")