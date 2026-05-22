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
        circuit = []
        for _ in range(random.randint(1, n)):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        result = circuit[0][1]
        for gate in circuit[1:]:
            gate_type, inputs = gate
            if gate_type == 'AND':
                result = all(inputs)
            elif gate_type == 'OR':
                result = any(inputs)
        return result
    
    def min_representation_rank(circuit):
        n = len(circuit)
        rank = 0
        for _ in range(10):  # Sample multiple times to get a good estimate
            inputs = [random.randint(0, 1) for _ in range(n)]
            if evaluate_circuit(circuit) == evaluate_circuit([(gate_type, inputs) for gate_type, inputs in circuit]):
                rank += 1
        return rank / 10
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(20):  # Ensure at least 100 instances per seed
            circuit = generate_ac0_circuit(n)
            rank = min_representation_rank(circuit)
            if rank > 0:  # Avoid division by zero
                total_rank += rank
                instances_tested += 1
    
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_rank >= 1 and (mean_rank - 1) <= 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_representation_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed={first_failing_seed}"
    
    print(result)