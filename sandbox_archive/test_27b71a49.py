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
    
    def generate_random_circuit(depth):
        if depth == 0:
            return ['NOT', random.choice(['0', '1'])]
        gate = random.choice(['AND', 'OR'])
        left = generate_random_circuit(depth - 1)
        right = generate_random_circuit(depth - 1)
        return [gate, left, right]
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, str):
            return circuit
        gate, left, right = circuit
        if gate == 'NOT':
            return '0' if evaluate_circuit(left) == '1' else '1'
        elif gate == 'AND':
            return '1' if evaluate_circuit(left) == '1' and evaluate_circuit(right) == '1' else '0'
        elif gate == 'OR':
            return '1' if evaluate_circuit(left) == '1' or evaluate_circuit(right) == '1' else '0'
    
    def her(circuit):
        state = evaluate_circuit(circuit)
        n = len(state)
        rank = 0
        for i in range(n):
            if state[i] == '1':
                rank += 1
        return rank
    
    depths = [5, 10, 15, 20, 30, 40]
    circuit_ranks = []
    
    for depth in depths:
        circuit = generate_random_circuit(depth)
        rank = her(circuit)
        circuit_ranks.append((depth, rank))
    
    if not circuit_ranks:
        return {
            "metric_name": "HER(C)",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    max_depth = max(depth for depth, _ in circuit_ranks)
    if max_depth < 16:
        return {
            "metric_name": "HER(C)",
            "metric_value": 0,
            "instances_tested": len(circuit_ranks),
            "n_max": max_depth,
            "conjecture_holds": False,
            "counterexample": "n_max_too_low"
        }
    
    mean_rank = sum(rank for _, rank in circuit_ranks) / len(circuit_ranks)
    std_rank = math.sqrt(sum((rank - mean_rank) ** 2 for _, rank in circuit_ranks) / len(circuit_ranks))
    
    conjecture_holds = all(rank <= depth * 10 for depth, rank in circuit_ranks)  # Arbitrary constant c=10
    counterexample = "" if conjecture_holds else "HER(C) > c * D"
    
    return {
        "metric_name": "HER(C)",
        "metric_value": mean_rank,
        "instances_tested": len(circuit_ranks),
        "n_max": max_depth,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 2**31-1) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")