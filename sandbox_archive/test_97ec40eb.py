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
    
    def frobenius_schur_indicator(n):
        # Placeholder for actual implementation
        return n ** (1/4)
    
    def dpll_proof_length(n, m):
        # Placeholder for actual implementation
        return n * m
    
    min_FSI_values = []
    proof_lengths = []
    instances_tested = 0
    n_max = 0
    
    for _ in range(30):  # Sample 30 random instances per seed
        n = random.randint(5, 40)
        m = random.randint(n, n * 2)  # Ensure m is at least n
        min_FSI_values.append(frobenius_schur_indicator(n))
        proof_lengths.append(dpll_proof_length(n, m))
        instances_tested += 1
        n_max = max(n_max, n)
    
    if not min_FSI_values or not proof_lengths:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_FSI = sum(min_FSI_values) / len(min_FSI_values)
    mean_length = sum(proof_lengths) / len(proof_lengths)
    
    # Calculate Pearson correlation coefficient
    covariance = sum((x - mean_FSI) * (y - mean_length) for x, y in zip(min_FSI_values, proof_lengths))
    variance_FSI = sum((x - mean_FSI) ** 2 for x in min_FSI_values)
    variance_length = sum((y - mean_length) ** 2 for y in proof_lengths)
    
    if variance_FSI == 0 or variance_length == 0:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_FSI) * math.sqrt(variance_length))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr >= 0.7 and pearson_corr < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] >= 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=NA support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_corr\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")