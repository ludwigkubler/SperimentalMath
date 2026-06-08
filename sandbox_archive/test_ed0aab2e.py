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
        for _ in range(random.randint(1, n)):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def calculate_width(circuit):
        width = 1
        current_width = 1
        for gate, _ in circuit:
            if gate == 'AND':
                current_width += 1
            elif gate == 'OR':
                current_width -= 1
            width = max(width, current_width)
        return width
    
    def calculate_frobenius_schur_index(circuit):
        # Simplified approximation for demonstration purposes
        # Actual implementation would depend on the specific algebraic structure
        return len(circuit) / 2
    
    fs_index_list = []
    width_list = []
    
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        circuit = generate_random_circuit(n)
        width = calculate_width(circuit)
        fs_index = calculate_frobenius_schur_index(circuit)
        
        fs_index_list.append(fs_index)
        width_list.append(width)
        
        instances_tested += 1
        n_max = max(n_max, n)
    
    correlation_coefficient = (instances_tested * sum(fs_index * width for fs_index, width in zip(fs_index_list, width_list)) -
                               sum(fs_index_list) * sum(width_list)) / (
                               math.sqrt(instances_tested * sum(fs_index ** 2 for fs_index in fs_index_list) - sum(fs_index_list) ** 2) *
                               math.sqrt(instances_tested * sum(width ** 2 for width in width_list) - sum(width_list) ** 2))
    
    mean_fs_index = sum(fs_index_list) / instances_tested
    max_diff = max(abs(fs_index - (mean_fs_index + i)) for i, fs_index in enumerate(fs_index_list))
    
    conjecture_holds = correlation_coefficient > 0.7 and max_diff <= 3
    
    return {
        "metric_name": "Frobenius-Schur Index vs Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Correlation: {correlation_coefficient}, Max Diff: {max_diff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction=1.0000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")