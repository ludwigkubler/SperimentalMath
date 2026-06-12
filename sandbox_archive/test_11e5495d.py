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
    
    def generate_protocol(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def p_adic_expansion(protocol, p=2):
        n = len(protocol)
        expansion = []
        for i in range(n):
            bit = protocol[i]
            if bit == 1:
                expansion.append(1)
            else:
                expansion.append(0)
        return expansion
    
    def variance(bits):
        mean = sum(bits) / len(bits)
        return sum((x - mean) ** 2 for x in bits) / len(bits)
    
    def rank(expansion):
        n = len(expansion)
        if n == 0:
            return 0
        max_rank = 1
        for i in range(1, n):
            if expansion[i] != expansion[0]:
                max_rank += 1
        return max_rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_variance = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            protocol = generate_protocol(n)
            p_adic_expansion_value = p_adic_expansion(protocol)
            rank_value = rank(p_adic_expansion_value)
            variance_value = variance(protocol)
            
            total_rank += rank_value
            total_variance += variance_value
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_rank = total_rank / instances_tested
    mean_variance = total_variance / instances_tested
    
    correlation_coefficient = (instances_tested * sum(rank_value * variance_value for rank_value, variance_value in zip(p_adic_expansion_value, protocol)) - total_rank * total_variance) / \
                               math.sqrt((instances_tested * sum(rank_value ** 2 for rank_value in p_adic_expansion_value) - total_rank ** 2) * (instances_tested * sum(variance_value ** 2 for variance_value in protocol) - total_variance ** 2))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")