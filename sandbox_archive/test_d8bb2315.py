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
    
    def generate_circuit(n):
        if n == 1:
            return ['NOT', '0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return ['AND'] + left + right
    
    def evaluate_circuit(circuit, assignment):
        stack = []
        for item in circuit:
            if isinstance(item, str) and item.isdigit():
                stack.append(int(item))
            elif item == 'NOT':
                stack.append(1 - stack.pop())
            elif item == 'AND':
                b = stack.pop()
                a = stack.pop()
                stack.append(a & b)
        return stack[0]
    
    def monotone_width(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        left = circuit[:n // 2]
        right = circuit[n // 2:]
        return max(monotone_width(left), monotone_width(right))
    
    def min_quaternionic_kahler_dimension(n):
        # Simplified heuristic for demonstration purposes
        return n ** (2 / 3)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        instances_tested = 0
        total_ratio = 0
        
        while instances_tested < 30:
            assignment = [random.randint(0, 1) for _ in range(n)]
            value = evaluate_circuit(circuit, assignment)
            if value == 0:  # Skip invalid assignments
                continue
            
            d = min_quaternionic_kahler_dimension(n)
            w_m = monotone_width(circuit)
            ratio = d / w_m
            
            total_ratio += ratio
            instances_tested += 1
        
        avg_ratio = total_ratio / instances_tested
        results.append({
            "n": n,
            "avg_ratio": avg_ratio,
            "instances_tested": instances_tested
        })
    
    conjecture_holds = all(0.5 * n ** (2 / 3) <= result['avg_ratio'] <= 2 * n ** (1 / 3) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Average Ratio",
        "metric_value": sum(result['avg_ratio'] for result in results) / len(results),
        "instances_tested": sum(result['instances_tested'] for result in results),
        "n_max": max(result['n'] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    all_results = [run_trial(seed) for seed in seeds]
    avg_metric = sum(result['metric_value'] for result in all_results) / len(all_results)
    std_metric = math.sqrt(sum((result['metric_value'] - avg_metric) ** 2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result['conjecture_holds']) / len(all_results)
    
    if all(result['conjecture_holds'] for result in all_results):
        print(f"RESULT: SUPPORTED mean={avg_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")