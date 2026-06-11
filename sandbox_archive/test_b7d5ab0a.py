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
    n = 30
    d = {}
    for i in range(n):
        phi = [random.choice([True, False]) for _ in range(2**i)]
        d[i] = phi
    
    def clause_indicator_polynomial(phi):
        return sum(phi[i] * (1 << i) for i in range(len(phi)))
    
    def p_adic_hausdorff_dimension(p, chi):
        # Placeholder implementation
        return len(chi)
    
    def dpll_search_tree_height(phi):
        if not phi:
            return 0
        if all(not x for x in phi):
            return 0
        return 1 + max(dpll_search_tree_height([x for x in phi if not x]), dpll_search_tree_height([not x for x in phi if x]))
    
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for i in range(5, 41):
        chi = clause_indicator_polynomial(d[i])
        h = p_adic_hausdorff_dimension(i, chi)
        h_dpll = dpll_search_tree_height(chi)
        
        if h_dpll == 0:
            continue
        
        metric_values.append(h / h_dpll)
        instances_tested += 1
        n_max = max(n_max, i)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in metric_values) / len(metric_values))
    
    correlation_coefficient = (sum((metric_values[i] - mean_metric_value) * (i - n_max) for i in range(instances_tested)) /
                               (instances_tested * std_metric_value * math.sqrt(n_max**2 - n_max)))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": "" if abs(correlation_coefficient) >= 0.9 else "Correlation coefficient out of expected range"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.9) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient out of expected range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")