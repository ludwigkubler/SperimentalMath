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

def generate_circuit(n, D):
    if n == 1:
        return [[0], [1]]  # Base case: a circuit with one input and two outputs
    
    subcircuit = generate_circuit(n // 2, D - 1)
    
    new_circuit = []
    for i in range(2 ** (n // 2)):
        new_input = [i >> j & 1 for j in range(n // 2)]
        output = [subcircuit[i][j] ^ subcircuit[i + 1][j] for j in range(D - 1)]
        new_circuit.append(new_input + output)
    
    return new_circuit

def compute_entropy(circuit):
    n = len(circuit[0])
    state_space_size = 2 ** n
    transition_matrix = [[0] * state_space_size for _ in range(state_space_size)]
    
    for i in range(state_space_size):
        for j in range(state_space_size):
            if circuit[i][n:] == circuit[j][:D - 1]:
                transition_matrix[i][j] += 1
    
    # Normalize the transition matrix
    for row in transition_matrix:
        total = sum(row)
        if total > 0:
            for j in range(len(row)):
                row[j] /= total
    
    # Compute the entropy of each state
    entropies = []
    for i in range(state_space_size):
        p = [transition_matrix[i][j] / sum(transition_matrix[i]) for j in range(state_space_size)]
        entropy = -sum(p[j] * math.log2(p[j]) if p[j] > 0 else 0 for j in range(len(p)))
        entropies.append(entropy)
    
    # The topological entropy is the maximum entropy of any state
    return max(entropies)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size 5 times to ensure statistical signal
            circuit = generate_circuit(n, random.randint(1, min(3, n)))
            depth = len(circuit[0]) - n
            entropy = compute_entropy(circuit)
            total_metric_value += entropy / depth
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(entropy / depth <= depth * math.log2(2 ** (depth + 1)) for circuit in generate_circuit(n, random.randint(1, min(3, n))) for depth in range(1, len(circuit[0]) - n + 1) for entropy in [compute_entropy(circuit)])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Topological Entropy per Variable",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    all_results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")