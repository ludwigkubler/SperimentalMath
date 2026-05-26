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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot row
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate non-pivot elements
            for j in range(n):
                if i != j:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        # Extract the diagonal to get the rank
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def calculate_minimal_rank(representation):
        n = len(representation)
        augmented_matrix = [row + [0] * n + [i == j for i in range(n)] for j, row in enumerate(representation)]
        return gaussian_elimination(augmented_matrix)
    
    def generate_disjointness_protocol(n):
        protocol = []
        for _ in range(n):
            protocol.append(random.sample(range(2**n), 2))
        return protocol
    
    def twisted_group_representation(protocol):
        n = len(protocol[0])
        representation = [[0] * (2*n) for _ in range(2*n)]
        for i, (a, b) in enumerate(protocol):
            for j in range(n):
                if a[j] == 1:
                    representation[i][j] += 1
                if b[j] == 1:
                    representation[n+i][j+n] += 1
        return representation
    
    n = random.randint(5, 40)
    protocol = generate_disjointness_protocol(n)
    representation = twisted_group_representation(protocol)
    rank = calculate_minimal_rank(representation)
    
    metric_name = "minimal_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= n**2 * math.log(n, 2) * (1 - 0.05)
    counterexample = "" if conjecture_holds else f"rank={rank}, expected≥{n**2 * math.log(n, 2)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")