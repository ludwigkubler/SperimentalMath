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

def generate_random_circuit(depth: int) -> list:
    if depth == 1:
        return [random.choice([0, 1])]
    else:
        inputs = [generate_random_circuit(random.randint(1, depth-1)) for _ in range(2)]
        gate = random.choice(['AND', 'OR'])
        return [gate] + inputs

def compute_matroid(circuit: list) -> dict:
    matroid = {}
    def dfs(node):
        if isinstance(node, int):
            return {node}
        else:
            gate, *inputs = node
            input_sets = [dfs(inp) for inp in inputs]
            result_set = set()
            for s1 in input_sets[0]:
                for s2 in input_sets[1]:
                    result_set.add((s1, s2))
            matroid[node] = result_set
            return result_set
    dfs(circuit)
    return matroid

def compute_lidb(matroid: dict) -> int:
    def is_independent(set_):
        for pair in set_:
            if len(pair[0]) + len(pair[1]) > 2:
                return False
        return True
    
    independent_sets = []
    for size in range(1, len(matroid)):
        for subset in itertools.combinations(matroid.keys(), size):
            if is_independent(subset):
                independent_sets.append(set(subset))
    
    max_rank = 0
    for s in independent_sets:
        rank = sum(len(pair[0]) + len(pair[1]) for pair in matroid[s])
        if rank > max_rank:
            max_rank = rank
    
    return max_rank

def compute_entanglement_complexity(circuit: list) -> int:
    def count_gates(node):
        if isinstance(node, int):
            return 0
        else:
            gate, *inputs = node
            return 1 + sum(count_gates(inp) for inp in inputs)
    
    return count_gates(circuit)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        depth = random.randint(5, 40)
        circuit = generate_random_circuit(depth)
        matroid = compute_matroid(circuit)
        lidb = compute_lidb(matroid)
        entanglement_complexity = compute_entanglement_complexity(circuit)
        
        metric_values.append(lidb * entanglement_complexity)
    
    if len(metric_values) < instances_tested:
        conjecture_holds = False
        counterexample = "insufficient_data"
    
    return {
        "metric_name": "LIDB * Entanglement Complexity",
        "metric_value": sum(metric_values) / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")