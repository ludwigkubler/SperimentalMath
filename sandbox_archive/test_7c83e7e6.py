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
    
    def generate_random_circuit(n):
        if n == 1:
            return ['0']
        elif n == 2:
            return ['0', '1', 'XOR(0, 1)']
        else:
            subcircuit = generate_random_circuit(random.randint(1, n-1))
            gate = random.choice(['AND', 'OR'])
            return [f'{gate}({subcircuit[i]}, {subcircuit[i+1]})' for i in range(len(subcircuit)-1)]
    
    def compute_ranks(circuits):
        ranks = []
        for circuit in circuits:
            rank = 0
            for gate in circuit.split(','):
                if 'AND' in gate or 'OR' in gate:
                    rank += 1
            ranks.append(rank)
        return ranks
    
    def compute_widths(circuits):
        widths = []
        for circuit in circuits:
            width = len(circuit.split(',')) - 1
            widths.append(width)
        return widths
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        circuits = generate_random_circuit(n)
        ranks.extend(compute_ranks(circuits))
        widths.extend(compute_widths(circuits))
    
    if not ranks or not widths:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": len(ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_circuit"
        }
    
    correlation = sum((r - mean(ranks)) * (w - mean(widths)) for r, w in zip(ranks, widths)) / (len(ranks) * std(ranks) * std(widths))
    mean_diff = abs(mean(ranks) - mean(widths))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and mean_diff <= 3,
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

def std(lst):
    avg = mean(lst)
    variance = sum((x - avg) ** 2 for x in lst) / len(lst)
    return math.sqrt(variance)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold\" first_failing_seed={first_failing_seed}")