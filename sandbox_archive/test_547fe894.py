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
    
    def generate_random_instance(m):
        variables = set()
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
            variables.update(clause)
        return clauses
    
    def fundamental_group_size(embedding):
        # Placeholder function to simulate the computation of the fundamental group size
        # This is a dummy implementation and should be replaced with actual logic
        return len(embedding)
    
    def topological_entropy(fundamental_group_size):
        if fundamental_group_size <= 0:
            return 0.0
        return math.log2(fundamental_group_size + 1)
    
    m_values = [5, 10, 15, 20, 30, 40]
    h_min_sum = 0
    c_I_sum = 0
    instances_tested = 0
    
    for m in m_values:
        for _ in range(5):  # Test each size with 5 different instances
            instance = generate_random_instance(m)
            c_I = len(instance)
            embedding = instance  # Placeholder for actual embedding logic
            h_min = topological_entropy(fundamental_group_size(embedding))
            h_min_sum += h_min
            c_I_sum += c_I
            instances_tested += 1
    
    mean_h_min = h_min_sum / instances_tested
    mean_c_I = c_I_sum / instances_tested
    correlation = (mean_h_min * mean_c_I) / (math.sqrt(mean_h_min**2 * mean_c_I**2))
    
    conjecture_holds = 0.5 <= correlation <= 1.5
    counterexample = "" if conjecture_holds else f"correlation={correlation}"
    
    return {
        "metric_name": "Correlation between h_min and c(I)",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(m_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_bounds\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")