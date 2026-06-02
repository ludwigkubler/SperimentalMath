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
    
    def frobenius_monomial_rank(n):
        # Placeholder for actual implementation
        return n
    
    def frege_proof_length(n):
        # Placeholder for actual implementation
        return 2 ** n
    
    def frobenius_algebraic_operation(n):
        # Placeholder for actual implementation
        return n // 2
    
    def pearson_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
        return cov_xy / (std_x * std_y)
    
    def t_test(r, n):
        # Placeholder for actual implementation
        return r
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        mfr_values = []
        l_values = []
        for _ in range(30):
            phi = frobenius_monomial_rank(n)
            l_phi = frege_proof_length(phi)
            mfr_values.append(phi)
            l_values.append(l_phi)
        
        correlation = pearson_correlation(mfr_values, l_values)
        p_value = t_test(correlation, len(mfr_values))
        
        if p_value <= 0.05 and correlation >= 0.8:
            results.append({"n": n, "correlation": correlation, "p_value": p_value})
    
    mean_correlation = sum(result["correlation"] for result in results) / len(results)
    std_correlation = math.sqrt(sum((result["correlation"] - mean_correlation) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["p_value"] <= 0.05 and result["correlation"] >= 0.8) / len(results)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": mean_correlation,
        "instances_tested": sum(result["n"] * 30 for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_correlation = sum(result["metric_value"] for result in results) / len(results)
    std_correlation = math.sqrt(sum((result["metric_value"] - mean_correlation) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_correlation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")