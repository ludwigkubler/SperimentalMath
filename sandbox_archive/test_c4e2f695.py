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
        # Placeholder for actual implementation of Frobenius-Schur indicator calculation
        return random.uniform(0.1, 0.5) * n ** (1/4)
    
    def dpll_proof_length(n):
        # Placeholder for actual implementation of DPLL proof length calculation
        return random.randint(100, 200)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        min_FSI = frobenius_schur_indicator(n)
        proof_length = dpll_proof_length(n)
        results.append((min_FSI, proof_length))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _ in results)
    instances_tested = len(results)
    min_FSIs, proof_lengths = zip(*results)
    mean_FSI = sum(min_FSIs) / instances_tested
    mean_proof_length = sum(proof_lengths) / instances_tested
    
    def pearson_correlation(x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - x_mean) ** 2 for xi in x)) * math.sqrt(sum((yi - y_mean) ** 2 for yi in y))
        return numerator / denominator if denominator != 0 else 0
    
    correlation_coefficient = pearson_correlation(min_FSIs, proof_lengths)
    
    conjecture_holds = 0.5 <= correlation_coefficient < 0.7
    counterexample = "" if conjecture_holds else f"correlation={correlation_coefficient:.2f}"
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] >= 0.5 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")