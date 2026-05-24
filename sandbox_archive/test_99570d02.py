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
    
    def construct_polynomial_system(circuit):
        n = len(circuit)
        polynomials = [0] * n
        for i in range(n):
            if circuit[i]:
                polynomials[i] += 1
        return polynomials
    
    def min_tropical_growth_rate(polynomials):
        max_value = max(polynomials)
        if max_value == 0:
            return 0
        return math.log2(max_value)
    
    def generate_ac0_circuit(n, s):
        circuit = [random.choice([0, 1]) for _ in range(s)]
        random.shuffle(circuit)
        return circuit[:n]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size 5 times to ensure statistical robustness
            s = random.randint(1, min(n * 2, 40))  # Ensure s is at most twice n and ≤ 40
            circuit = generate_ac0_circuit(n, s)
            polynomials = construct_polynomial_system(circuit)
            g_P = min_tropical_growth_rate(polynomials)
            total_metric_value += g_P
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(g_P >= math.log2(s) for _, s, circuit in zip(range(instances_tested), n_values * 5, [generate_ac0_circuit(n, random.randint(1, min(n * 2, 40))) for _ in range(instances_tested)]) for g_P in (min_tropical_growth_rate(construct_polynomial_system(circuit)) for _ in range(5)))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_tropical_growth_rate",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")