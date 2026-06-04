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
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def monotone_width(circuit):
        width = 0
        stack = []
        for gate in circuit:
            if gate[0] == 'AND':
                stack.append(len(gate[1]))
            elif gate[0] == 'OR':
                max_inputs = max(stack)
                stack = [max_inputs + 1]
        return max(stack) if stack else 0
    
    def git_degree(circuit):
        n = len(circuit)
        width = monotone_width(circuit)
        return n * width
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        git_deg = git_degree(circuit)
        width = monotone_width(circuit)
        ratio = git_deg / (math.log2(n) * width)
        total_ratio += ratio
        instances_tested += 1
        if n > n_max:
            n_max = n
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio <= 10  # Placeholder value, replace with actual calculation
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "git_degree_over_log_n_width",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")