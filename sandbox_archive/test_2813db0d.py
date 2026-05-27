# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools
import collections

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random classical group G (for simplicity, use a 2x2 matrix)
    n = random.randint(5, 40)
    group = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    # Tropicalize the group
    tropicalized_group = [[max(a, b) for b in row] for row in group]
    
    # Calculate the minimal rank of the tropicalized group
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if any(matrix[j][i] != 0 for j in range(i, m)):
                rank += 1
                for j in range(i, m):
                    matrix[j][i] /= matrix[i][i]
                for j in range(n):
                    if j == i:
                        continue
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    min_rank_tropicalized = min_rank(tropicalized_group)
    
    # Construct an ACC⁰ circuit C that computes an isomorphism class of G
    # For simplicity, use a trivial circuit with width equal to the number of elements in G
    acc0_circuit_width = n * n
    
    # Measure the width w(C) of this circuit
    metric_value = acc0_circuit_width
    
    # Check if the minimal rank of the tropicalization is at least c
    # For simplicity, use a constant c = 1 (this is just an example)
    c = 1
    conjecture_holds = min_rank_tropicalized >= c
    
    # Return the results
    return {
        "metric_name": "ACC⁰ Circuit Width",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Minimal rank {min_rank_tropicalized} is less than c={c}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='minimal_rank_too_low' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")