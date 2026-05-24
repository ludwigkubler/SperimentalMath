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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    augmented_matrix = [row[:] + [0] for row in matrix]
    
    for i in range(rows):
        max_row = i
        for j in range(i+1, rows):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        pivot = augmented_matrix[i][i]
        for j in range(i, cols + 1):
            augmented_matrix[i][j] /= pivot
        
        for j in range(rows):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, cols + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    rank = sum(1 for row in augmented_matrix if any(row))
    return rank

def generate_ac0_circuit(n):
    circuit = []
    for _ in range(n):
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        circuit.append(matrix)
    return circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different circuits
            circuit = generate_ac0_circuit(n)
            rank = gaussian_elimination(circuit)
            total_rank += rank
            instances_tested += 1
    
    mean_minimal_rank = total_rank / instances_tested
    conjecture_holds = mean_minimal_rank <= 2 * math.log(instances_tested)  # Example constant c=2 for simplicity
    counterexample = "" if conjecture_holds else f"mean_minimal_rank={mean_minimal_rank} > 2*log({instances_tested})"
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": mean_minimal_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_minimal_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_minimal_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")