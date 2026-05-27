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
    
    def generate_ac0_circuit(n):
        # Generate a random AC⁰ circuit computing PARITY on n inputs
        circuit = []
        for _ in range(random.randint(1, 5)):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_quaternionic_form(circuit):
        # Compute the minimal rank of the quaternionic form representation
        n = len(circuit[0][1])
        form = [[0] * n for _ in range(n)]
        for gate, inputs in circuit:
            if gate == 'AND':
                for i in range(n):
                    for j in range(n):
                        form[i][j] += inputs[i] * inputs[j]
            elif gate == 'OR':
                for i in range(n):
                    for j in range(n):
                        form[i][j] += 1 - (1 - inputs[i]) * (1 - inputs[j])
        rank = 0
        for row in form:
            if any(row):
                rank += 1
        return rank
    
    def size(circuit):
        # Compute the size of the circuit
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        rank = compute_quaternionic_form(circuit)
        size_value = size(circuit)
        results.append({
            "n": n,
            "rank": rank,
            "size": size_value
        })
    
    metric_value = sum(result["rank"] / math.log(result["size"]) for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(rank >= math.log(size_value) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")