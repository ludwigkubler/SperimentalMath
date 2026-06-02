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
    
    def generate_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def clause_set_entropy(formula):
        count = formula.count('1')
        return count / len(formula) * math.log(count / len(formula)) + (len(formula) - count) / len(formula) * math.log((len(formula) - count) / len(formula))
    
    def algebraic_k_theory_order(n):
        # Simplified approximation for demonstration purposes
        return n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        entropy = clause_set_entropy(formula)
        order = algebraic_k_theory_order(n)
        results.append((order, log_n_times_entropy))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _ in results)
    instances_tested = len(results)
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in results) / math.sqrt(sum((x - mean_x)**2 for x, _ in results) * sum((y - mean_y)**2 for _, y in results))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.8 <= correlation_coefficient < 1.5,
        "counterexample": "" if 0.8 <= correlation_coefficient < 1.5 else "correlation_coefficient_out_of_bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] == "correlation_coefficient_out_of_bounds" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] == "correlation_coefficient_out_of_bounds")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")