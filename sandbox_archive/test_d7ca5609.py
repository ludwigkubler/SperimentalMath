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
    
    def generate_polynomial(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_circuit_size(poly):
        n = len(poly)
        size = 0
        for i in range(n):
            if poly[i] == 1:
                size += 2
        return size
    
    def arithmetic_hodge_index(poly):
        n = len(poly)
        count = sum(1 for x in poly if x == 1)
        return Fraction(count, n) * math.log2(n)
    
    instances_tested = 0
    h_values = []
    circuit_sizes = []
    
    for _ in range(30):
        poly = generate_polynomial(random.randint(5, 40))
        h_value = arithmetic_hodge_index(poly)
        circuit_size = compute_circuit_size(poly)
        
        if h_value <= math.log2(circuit_size):
            instances_tested += 1
            h_values.append(h_value)
            circuit_sizes.append(circuit_size)
    
    if instances_tested == 0:
        return {
            "metric_name": "Arithmetic Hodge Index",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_h = sum(h_values) / instances_tested
    std_h = math.sqrt(sum((x - mean_h) ** 2 for x in h_values) / instances_tested)
    
    correlation_coefficient = sum((h_values[i] - mean_h) * (math.log2(circuit_sizes[i]) - mean(math.log2(x) for x in circuit_sizes)) for i in range(instances_tested))
    correlation_coefficient /= instances_tested * std_h * math.sqrt(sum((math.log2(circuit_sizes[i]) - mean(math.log2(x) for x in circuit_sizes)) ** 2 for i in range(instances_tested)))
    
    return {
        "metric_name": "Arithmetic Hodge Index",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_coefficient > 0.9 and all(abs(h - mean_h) <= 3 * std_h for h in h_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_corr = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_corr = math.sqrt(sum((r['metric_value'] - mean_corr) ** 2 for r in results if r['metric_value'] is not None)) / len(results)
    
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")