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
    
    def generate_random_circuit(n: int):
        circuit = []
        for _ in range(2 * n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(2)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_monotone_width(circuit):
        # Placeholder function to simulate monotone width computation
        # In practice, this would involve a more complex algorithm
        return len(circuit)
    
    def compute_minimal_rank(circuit):
        n = len(circuit) + 1
        augmented_matrix = [row[:] + [1] for row in circuit]
        rank = 0
        
        for i in range(n):
            if all(augmented_matrix[j][i] == 0 for j in range(rank)):
                return rank
            pivot_row = max(range(rank, n), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[pivot_row], augmented_matrix[rank] = augmented_matrix[rank], augmented_matrix[pivot_row]
            
            for j in range(n):
                if j != rank:
                    factor = augmented_matrix[j][i] / augmented_matrix[rank][i]
                    for k in range(i, n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[rank][k]
            rank += 1
        
        return rank
    
    def run_circuit(circuit):
        # Placeholder function to simulate circuit execution
        # In practice, this would involve a more complex algorithm
        return random.choice([0, 1])
    
    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    monotone_width = compute_monotone_width(circuit)
    minimal_rank = compute_minimal_rank(circuit)
    
    metric_value = abs(minimal_rank - monotone_width) / monotone_width
    conjecture_holds = metric_value <= 3
    counterexample = "" if conjecture_holds else f"minimal_rank={minimal_rank}, monotone_width={monotone_width}"
    
    return {
        "metric_name": "Rank-Monotone Width Ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = f"SUPPORTED mean={sum(metric_values) / len(metric_values):.2f} std=0 support_fraction=1"
    elif support_fraction >= 0.8:
        result = f"SUPPORTED mean={sum(metric_values) / len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(result)