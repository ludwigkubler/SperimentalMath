# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools
import collections

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def construct_polynomial(phi):
        n = len(phi)
        poly = [0] * (2**n)
        for i in range(2**n):
            if phi[i // 2] == '1':
                poly[i] = 1
        return poly
    
    def dpll_width(phi, max_depth=1000):
        n = len(phi)
        stack = [(phi, 0)]
        visited = set()
        width = 0
        
        while stack:
            phi, depth = stack.pop()
            if phi in visited:
                continue
            visited.add(phi)
            
            if depth > max_depth:
                return float('inf')
            
            if all(c == '1' for c in phi):
                width = max(width, len(phi))
                continue
            
            split_index = phi.find('0')
            if split_index == -1:
                split_index = 0
            
            left_phi = phi[:split_index] + '1' + phi[split_index+1:]
            right_phi = phi[:split_index] + '0' + phi[split_index+1:]
            
            stack.append((left_phi, depth + 1))
            stack.append((right_phi, depth + 1))
        
        return width
    
    def local_ring_rank(poly):
        n = len(poly)
        ring = [0] * (2**n)
        for i in range(2**n):
            if poly[i] == 1:
                ring[i] = 1
        
        rank = 0
        while any(x != 0 for x in ring):
            non_zero_indices = [i for i, x in enumerate(ring) if x != 0]
            min_index = min(non_zero_indices)
            min_value = ring[min_index]
            
            for i in range(2**n):
                if ring[i] % min_value == 0:
                    ring[i] //= min_value
            
            rank += 1
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_width = 0
    total_rank = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            phi = generate_instance(n)
            poly = construct_polynomial(phi)
            width = dpll_width(phi)
            rank = local_ring_rank(poly)
            
            if width == float('inf'):
                continue
            
            instances_tested += 1
            total_width += width
            total_rank += rank
            max_n = max(max_n, n)
    
    mean_width = total_width / instances_tested
    mean_rank = total_rank / instances_tested
    
    correlation_coefficient = (instances_tested * sum(w * r for w, r in zip(widths, ranks)) - 
                               sum(widths) * sum(ranks)) / math.sqrt(
                                   (instances_tested * sum(w**2 for w in widths) - sum(widths)**2) *
                                   (instances_tested * sum(r**2 for r in ranks) - sum(ranks)**2))
    
    conjecture_holds = correlation_coefficient > 0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient_too_low"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                                            31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 
                                            73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")