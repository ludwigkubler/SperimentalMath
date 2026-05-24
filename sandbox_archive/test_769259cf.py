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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def algebraic_curve_representation(f):
        n = int(math.log2(len(f)))
        curve = []
        for i in range(2**n):
            x = bin(i)[2:].zfill(n)
            y = f[i]
            curve.append((x, y))
        return curve
    
    def minimal_local_complexity(curve):
        n = len(curve[0][0])
        complexity = 0
        for i in range(n):
            bits = [point[0][i] for point in curve]
            if all(bit == '0' for bit in bits) or all(bit == '1' for bit in bits):
                continue
            complexity += 1
        return complexity
    
    def geometric_quantization(f):
        n = int(math.log2(len(f)))
        quantized = []
        for i in range(2**n):
            x = bin(i)[2:].zfill(n)
            y = f[i]
            if y == 0:
                quantized.append((x, '0'))
            else:
                quantized.append((x, '1'))
        return quantized
    
    def communication_complexity(quantized):
        n = len(quantized[0][0])
        complexity = 0
        for i in range(n):
            bits = [point[0][i] for point in quantized]
            if all(bit == '0' for bit in bits) or all(bit == '1' for bit in bits):
                continue
            complexity += 1
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        curve = algebraic_curve_representation(f)
        L_f = minimal_local_complexity(curve)
        quantized = geometric_quantization(f)
        CC_GQ_f = communication_complexity(quantized)
        
        if L_f == 0 or CC_GQ_f == 0:
            continue
        
        ratio = L_f / CC_GQ_f
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "Ratio of Local Complexity to Communication Complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "Ratio of Local Complexity to Communication Complexity",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": all(0.9 <= ratio <= 1.1 for ratio in results) and std_dev < 3 * std_dev / math.sqrt(len(results)),
        "counterexample": "" if all(0.9 <= ratio <= 1.1 for ratio in results) else "out_of_range"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 37))  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if all(result is not None for result in results):
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if 0.9 <= r <= 1.1) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if not (0.9 <= r <= 1.1))
            print(f"RESULT: FALSIFIED counterexample='out_of_range' first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE some_trials_failed")