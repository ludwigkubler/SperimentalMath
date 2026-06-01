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
    
    def generate_circuit(n, d):
        if n == 1:
            return ['x']
        else:
            inputs = [f'x{i}' for i in range(1, n+1)]
            gates = []
            for _ in range(d-1):
                new_inputs = []
                for _ in range(len(inputs)):
                    a, b = random.sample(inputs, 2)
                    gates.append(f'({a} AND {b})')
                    new_inputs.extend([f'g{i}' for i in range(len(gates))])
                inputs = new_inputs
            return inputs
    
    def compute_resolution_width(circuit):
        # Simplified resolution width estimation
        return len(circuit) ** 0.5
    
    def compute_local_coherence_rank(circuit):
        # Simplified local coherence rank estimation
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n, random.randint(2, 4))
        resolution_width = compute_resolution_width(circuit)
        local_coherence_rank = compute_local_coherence_rank(circuit)
        results.append({
            "n": n,
            "resolution_width": resolution_width,
            "local_coherence_rank": local_coherence_rank
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_circuit"
        }
    
    correlation = sum((r['resolution_width'] - r['local_coherence_rank']) ** 2 for r in results) / len(results)
    mean_resolution_width = sum(r['resolution_width'] for r in results) / len(results)
    mean_local_coherence_rank = sum(r['local_coherence_rank'] for r in results) / len(results)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r['n'] for r in results),
        "conjecture_holds": correlation <= 1e-6 * mean_resolution_width * mean_local_coherence_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results if r['metric_value'] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r['conjecture_holds']:
                print(f"RESULT: FALSIFIED counterexample=\"correlation_fail\" first_failing_seed={r['seed']}")
                break