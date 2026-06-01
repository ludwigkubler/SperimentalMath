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
    
    def construct_circuit(f):
        n = int(math.log2(len(f)))
        circuit = []
        for i in range(n):
            circuit.append((i, f[i]))
        return circuit
    
    def p_adic_divergence(c1, c2):
        if len(c1) != len(c2):
            return float('inf')
        n = len(c1)
        diff = 0
        for i in range(n):
            if c1[i] != c2[i]:
                diff += 1 / (n - i)
        return diff
    
    def communication_complexity(circuit):
        n = int(math.log2(len(circuit)))
        return n
    
    def correlation_analysis(data):
        n = len(data)
        x_sum = sum(d['min_d'] for d in data)
        y_sum = sum(d['c'] for d in data)
        xy_sum = sum(d['min_d'] * d['c'] for d in data)
        x2_sum = sum(d['min_d'] ** 2 for d in data)
        y2_sum = sum(d['c'] ** 2 for d in data)
        
        if n == 0:
            return {'r': float('nan'), 'mean_diff': float('nan')}
        
        numerator = n * xy_sum - x_sum * y_sum
        denominator = math.sqrt((n * x2_sum - x_sum ** 2) * (n * y2_sum - y_sum ** 2))
        
        if denominator == 0:
            return {'r': float('nan'), 'mean_diff': float('nan')}
        
        r = numerator / denominator
        mean_diff = abs(x_sum / n - y_sum / n)
        
        return {'r': r, 'mean_diff': mean_diff}
    
    data = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        c_f = construct_circuit(f)
        min_d = p_adic_divergence(c_f, [(i, 0) for i in range(n)])
        c = communication_complexity(c_f)
        data.append({'min_d': min_d, 'c': c})
    
    correlation_result = correlation_analysis(data)
    r = correlation_result['r']
    mean_diff = correlation_result['mean_diff']
    
    conjecture_holds = (abs(r) >= 0.7 and mean_diff <= 3)
    counterexample = "" if conjecture_holds else f"r={r}, mean_diff={mean_diff}"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": r,
        "instances_tested": len(data),
        "n_max": max(d['c'] for d in data),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r['metric_value'] for r in results) / len(results)
    std_r = math.sqrt(sum((r['metric_value'] - mean_r) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"r={results[seeds.index(first_failing_seed)]['metric_value']}, mean_diff={results[seeds.index(first_failing_seed)]['mean_diff']}\" first_failing_seed={first_failing_seed}")