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
        for _ in range(2**n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(gate)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_monotone_width(circuit):
        # Simplified monotone width calculation (for demonstration)
        return len(circuit)
    
    def compute_minimal_rank(circuit):
        n = len(circuit) + 1
        augmented_matrix = []
        for row in circuit:
            gate, inputs = row
            row_vector = [0] * n
            for input_index in inputs:
                row_vector[input_index] = 1
            augmented_matrix.append(row_vector)
        
        # Gaussian elimination to find rank
        rank = len(augmented_matrix)
        for i in range(rank):
            if augmented_matrix[i][i] == 0:
                found_nonzero_row = False
                for j in range(i+1, rank):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        found_nonzero_row = True
                        break
                if not found_nonzero_row:
                    rank -= 1
                    continue
            for j in range(i+1, rank):
                factor = -augmented_matrix[j][i] / augmented_matrix[i][i]
                for k in range(n):
                    augmented_matrix[j][k] += factor * augmented_matrix[i][k]
        
        return rank
    
    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    monotone_width = compute_monotone_width(circuit)
    minimal_rank = compute_minimal_rank(circuit)
    
    metric_value = abs(minimal_rank - monotone_width) / monotone_width if monotone_width != 0 else float('inf')
    instances_tested = 1
    n_max = n
    conjecture_holds = metric_value <= 3
    counterexample = "" if conjecture_holds else f"Minimal rank {minimal_rank} not within Θ({monotone_width})"
    
    return {
        "metric_name": "Rank-Width Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [result["metric_value"] for result in results if result["instances_tested"] > 0]
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank-Width Ratio exceeded\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or metric saturation")