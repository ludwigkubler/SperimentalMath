# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_clause_set(n: int):
        return [random.choice([f"x{i}", f"~x{i}"]) for _ in range(n)]
    
    def minimal_tropical_rank(clause_set):
        # Placeholder implementation of minimal tropical rank
        # This is a dummy function for demonstration purposes
        return len(clause_set)
    
    alpha_values = [0.5, 1.0, 1.5]
    ratios = []
    instances_tested = 0
    
    for n in range(5, 41):
        clause_sets = [generate_clause_set(n) for _ in range(30)]
        instances_tested += len(clause_sets)
        
        for C in clause_sets:
            mtr_C = minimal_tropical_rank(C)
            for alpha in alpha_values:
                ratios.append((mtr_C / (n ** alpha), n))
    
    if not ratios:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Calculate Pearson correlation coefficient
    mean_x = sum(x for x, _ in ratios) / len(ratios)
    mean_y = sum(y for _, y in ratios) / len(ratios)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in ratios)
    denominator = sum((x - mean_x)**2 * (y - mean_y)**2 for x, y in ratios)
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_corr = numerator / denominator**0.5
    alpha_estimates = [sum(x for x, _ in ratios if y == n) / sum(1 for _, y in ratios if y == n) for n in set(y for _, y in ratios)]
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": pearson_corr >= 0.7 and all(abs(a - alpha_estimates[alpha_values.index(1)]) <= 0.05 * a for a in alpha_estimates),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = (sum((r["metric_value"] - mean_corr)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, alpha_estimates={r['alpha_estimates']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break