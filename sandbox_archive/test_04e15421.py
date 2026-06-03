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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def calculate_monotone_width(circuit):
        n = len(circuit[0][1])
        width = 0
        for i in range(n):
            max_ones = 0
            for j in range(2**n):
                if circuit[j][1][i] == 1:
                    max_ones += 1
            width = max(width, max_ones)
        return width
    
    def calculate_local_indeterminacy(circuit):
        n = len(circuit[0][1])
        indeterminacy = 0
        for i in range(n):
            ones_count = sum(1 for j in range(2**n) if circuit[j][1][i] == 1)
            zeros_count = 2**n - ones_count
            indeterminacy += abs(ones_count - zeros_count)
        return indeterminacy
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_random_circuit(n)
        w_mon = calculate_monotone_width(circuit)
        lind = calculate_local_indeterminacy(circuit)
        
        if w_mon == 0:
            continue
        
        metric_values.append((lind, w_mon))
    
    if not metric_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_metric_values"
        }
    
    linds, w_mons = zip(*metric_values)
    mean_lind = sum(linds) / len(linds)
    mean_w_mon = sum(w_mons) / len(w_mons)
    correlation_coefficient = (sum((l - mean_lind) * (w - mean_w_mon) for l, w in metric_values) /
                               math.sqrt(sum((l - mean_lind)**2 for l in linds) *
                                         sum((w - mean_w_mon)**2 for w in w_mons)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and abs(mean_lind / mean_w_mon - 1) <= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")