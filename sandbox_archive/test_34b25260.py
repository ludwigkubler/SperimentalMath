# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(n):
        coefficients = [random.randint(0, 1) for _ in range(n+1)]
        return lambda x: sum(c * (x ** i) for i, c in enumerate(coefficients))
    
    def compute_circuit_size(poly):
        # Simplified circuit size estimation
        degree = max([i for i, coeff in enumerate(poly.coefficients) if coeff != 0])
        return degree + 1
    
    instances_tested = 30
    h_values = []
    circuit_sizes = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        poly = generate_polynomial(n)
        h_value = sum(poly(x) ** 2 for x in range(-10, 11)) / (2 * (n + 1))
        circuit_size = compute_circuit_size(poly)
        
        h_values.append(h_value)
        circuit_sizes.append(circuit_size)
    
    mean_h = sum(h_values) / instances_tested
    mean_log2_circuits = sum(math.log2(x) for x in circuit_sizes) / instances_tested
    
    correlation_coefficient = sum((h_values[i] - mean_h) * (math.log2(circuit_sizes[i]) - mean_log2_circuits) for i in range(instances_tested)) / instances_tested
    std_deviation = math.sqrt(sum((x - mean_log2_circuits) ** 2 for x in circuit_sizes) / instances_tested)
    
    conjecture_holds = correlation_coefficient > 0.9 and all(abs(h_value - mean_h) <= 3 * std_deviation for h_value in h_values)
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9 or Hodge index exceeds average by more than 3 std deviations"
    
    return {
        "metric_name": "Arithmetic Hodge Index vs Circuit Size",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")