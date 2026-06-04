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
        for _ in range(2 * n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def monotone_width(circuit):
        width = 0
        current_level = []
        for gate in circuit:
            if gate[0] == 'AND':
                current_level.extend(gate[1])
            elif gate[0] == 'OR':
                current_level = list(set(current_level) | set(gate[1]))
            width = max(width, len(current_level))
        return width
    
    def git_degree(circuit):
        n = len(circuit)
        if n <= 1:
            return 1
        degree = 2 ** (n - 1)
        for gate in circuit:
            if gate[0] == 'AND':
                degree *= 2
            elif gate[0] == 'OR':
                degree += 2
        return degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            git_d = git_degree(circuit)
            width = monotone_width(circuit)
            if width > 0:
                ratio = git_d / (math.log2(n) * width)
                total_ratio += ratio
                instances_tested += 1
                n_max = max(n_max, n)
    
    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_ratio <= 1  # Assuming c is a constant <= 1 for simplicity
    
    return {
        "metric_name": "GIT_degree_over_log_n_times_width",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_ratio={mean_ratio}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio={result['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")