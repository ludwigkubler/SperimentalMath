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
        cnf = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def compute_quadratic_form(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for literal in clause:
                var = abs(literal) - 1
                Q[var][var] += 1
        return Q
    
    def min_quadratic_surface_area(Q):
        n = len(Q)
        area = 0
        for i in range(n):
            for j in range(i + 1, n):
                area += abs(Q[i][j])
        return area
    
    def volume(A):
        return A ** (3/2) / math.gamma(5/2)
    
    def frege_proof_width(cnf):
        # Placeholder function; actual implementation needed
        return len(cnf)
    
    instances_tested = 0
    n_max = 0
    total_area = 0
    total_volume = 0
    total_width = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        Q = compute_quadratic_form(cnf)
        area = min_quadratic_surface_area(Q)
        volume_val = volume(area)
        width = frege_proof_width(cnf)
        
        total_area += area
        total_volume += volume_val
        total_width += width
        
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_area = total_area / instances_tested
    mean_volume = total_volume / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * mean_area * mean_width - 
                               sum(area * width for area, width in zip([mean_area] * instances_tested, [mean_width] * instances_tested))) / \
                              math.sqrt((instances_tested * mean_area**2 - sum(area**2 for area in [mean_area] * instances_tested)) *
                                        (instances_tested * mean_width**2 - sum(width**2 for width in [mean_width] * instances_tested)))
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_volume <= 4 * mean_area
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}, Volume/Areas ratio: {mean_volume / mean_area}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["n_max"] for r in results) >= 16:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient or Volume/Areas ratio does not meet criteria\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data_or_budget_exceeded n_tested={len(results)}")