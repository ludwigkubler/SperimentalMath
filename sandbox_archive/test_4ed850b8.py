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
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_monotone_width(circuit):
        width = len(circuit)
        for i in range(len(circuit)):
            if all(circuit[j][1] == 0 for j in range(i+1)):
                width -= 1
        return width
    
    def compute_hyperbolic_rank(circuit):
        rank = 0
        for gate, inputs in circuit:
            rank += len(inputs)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank = 0
    total_width = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            rank = compute_hyperbolic_rank(circuit)
            width = compute_monotone_width(circuit)
            instances_tested += 1
            total_rank += rank
            total_width += width
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_rank = total_rank / instances_tested
    mean_width = total_width / instances_tested
    correlation = (instances_tested * sum(rank * width for rank, width in zip(ranks, widths)) - 
                   instances_tested * mean_rank * mean_width) / \
                  math.sqrt((instances_tested * sum(rank**2 for rank in ranks) - instances_tested * mean_rank**2) *
                            (instances_tested * sum(width**2 for width in widths) - instances_tested * mean_width**2))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8 and abs(mean_rank - mean_width) <= 3,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")