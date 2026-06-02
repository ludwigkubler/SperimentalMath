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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def entropy(s):
        counts = [s.count(c) for c in '01']
        total = sum(counts)
        if total == 0:
            return 0
        probabilities = [Fraction(count, total) for count in counts]
        return -sum(p * math.log2(p) for p in probabilities if p != 0)
    
    def algebraic_k_theory_order(n):
        # Placeholder function; actual implementation required
        return n
    
    instances_tested = 30
    n_max = 40
    correlation_sum = 0
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        formula = generate_boolean_formula(n)
        entropy_value = entropy(formula)
        order = algebraic_k_theory_order(n)
        
        if entropy_value <= 0:
            continue
        
        log_n_times_entropy = math.log2(n) * entropy_value
        correlation_sum += (order - log_n_times_entropy) / instances_tested
    
    mean_correlation = correlation_sum
    conjecture_holds = abs(mean_correlation) < 1.5 and abs(mean_correlation) >= 0.8
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result["metric_value"] > 1.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 1.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_greater_than_1.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")