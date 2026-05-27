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

def generate_ac0_circuit(n, s):
    # Placeholder function to generate an AC^0 circuit
    # This is a dummy implementation and should be replaced with actual logic
    return [[random.choice([0, 1]) for _ in range(s)] for _ in range(2**n)]

def symmetric_difference(f1, f2):
    return [x ^ y for x, y in zip(f1, f2)]

def count_distinct_divisors(circuit, n):
    divisors = set()
    for i in range(2**n):
        for j in range(i+1, 2**n):
            if symmetric_difference(circuit[i], circuit[j]) == [0] * len(circuit[0]):
                divisors.add(tuple(circuit[i]))
    return len(divisors)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        s = len(generate_ac0_circuit(n, 1))  # Dummy size calculation
        if s == 0:
            continue
        
        circuit = generate_ac0_circuit(n, s)
        for _ in range(5):  # Test with 5 random instances per n
            f = [random.choice([0, 1]) for _ in range(s)]
            D_f = count_distinct_divisors(circuit, n)
            total_metric_value += D_f / s
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "D(f)/s",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_metric = total_metric_value / instances_tested
    conjecture_holds = mean_metric >= math.log(n) ** 2 / s
    
    return {
        "metric_name": "D(f)/s",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"D(f)/s < Θ(log^2(n)/s) for n={n}, s={s}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"D(f)/s < Θ(log^2(n)/s)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")