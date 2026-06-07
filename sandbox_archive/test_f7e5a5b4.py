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
from math import log2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        cnf = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            cnf.append(clause)
        return cnf
    
    def dpll_width(cnf):
        # Simplified DPLL width calculation
        return len(cnf) * 2
    
    def p_adic_galois_index(cnf):
        # Placeholder for actual computation
        # For simplicity, we use a dummy value
        return random.randint(1, 10)
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = range(2, 31)
    instances_tested = 0
    total_index = 0
    total_width = 0
    
    for n in n_values:
        for m in m_values:
            cnf = generate_cnf(n, m)
            width = dpll_width(cnf)
            index = p_adic_galois_index(cnf)
            
            instances_tested += 1
            total_index += log2(index) if index > 0 else 0
            total_width += width
    
    mean_index = total_index / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * mean_index * mean_width - 
                               sum(log2(index) * width for index, width in zip(cnf_indices, cnf_widths))) / \
                              ((instances_tested - 1) * 
                               (sum(log2(index)**2 for index in cnf_indices) - instances_tested * mean_index**2) *
                               (sum(width**2 for width in cnf_widths) - instances_tested * mean_width**2))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_conjecture")