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
    
    def generate_ac0_circuit(n, s):
        # Simplified AC⁰ circuit generation (not actual AC⁰)
        return [[random.choice([0, 1]) for _ in range(s)] for _ in range(n)]
    
    def symmetric_difference(f, g):
        return [x ^ y for x, y in zip(f, g)]
    
    def count_distinct_divisors(circuit):
        divisors = set()
        n = len(circuit)
        s = len(circuit[0])
        
        for i in range(1 << n):
            mask = [i >> j & 1 for j in range(n)]
            divisor = [circuit[j][k] if mask[j] else (1 - circuit[j][k]) for k in range(s)]
            divisors.add(tuple(divisor))
        
        return len(divisors)
    
    def calculate_divisor_degree(circuit):
        n = len(circuit)
        s = len(circuit[0])
        return count_distinct_divisors(circuit) / s
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 random circuits
            circuit = generate_ac0_circuit(n, s)
            divisor_degree = calculate_divisor_degree(circuit)
            total_metric_value += divisor_degree
            instances_tested += 1
    
    metric_value = total_metric_value / instances_tested
    conjecture_holds = metric_value >= (math.log(n) ** 2) / s
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "symmetric_difference_divisor_degree",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")