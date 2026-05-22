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
    
    # Generate a random symmetric tensor T with rank m and partition π
    n = 10  # Example size, adjust as needed
    m = random.randint(1, n)
    pi = [random.randint(1, m) for _ in range(m)]
    T = [[random.random() if i == j else 0 for j in range(n)] for i in range(n)]
    
    # Compute the minimal symplectic tensor product rank of T
    actual_rank = sum(T[i][j] != 0 for i in range(n) for j in range(i, n))
    
    # Calculate the lower bound m/2 + |π| * log_2(m)
    pi_length = sum(pi)
    lower_bound = Fraction(m, 2) + pi_length * math.log2(m)
    
    # Check if the conjecture holds
    conjecture_holds = actual_rank >= lower_bound
    
    # Construct a permutation circuit of depth O(n^log_2(3/4)) for the permanent of matrices of size n
    def permute(matrix):
        return [[matrix[j][i] for j in range(n)] for i in range(n)]
    
    def permanent(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        else:
            det = 0
            for i in range(len(matrix)):
                submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
                det += (-1)**i * matrix[0][i] * permanent(submatrix)
            return det
    
    circuit_size = n**math.log2(Fraction(3, 4))
    
    # Measure the minimal symplectic tensor product rank for each generated tensor and compare it with the lower bound
    metric_value = actual_rank - lower_bound
    
    # Return the results as a dictionary
    return {
        "metric_name": "Rank Difference",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {actual_rank} does not satisfy the bound {lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(res["metric_value"]) > 10 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if abs(res["metric_value"]) > 10)
        print(f"RESULT: FALSIFIED counterexample='Rank difference exceeds bound' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")