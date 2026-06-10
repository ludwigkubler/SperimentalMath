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
    
    # Define the parameters for the trial
    m = 5  # Number of sender-receiver pairs
    n_max = 40  # Maximum input size
    
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):  # Run 30 trials per seed
        n = random.randint(5, n_max)  # Random input size between 5 and n_max
        communication_matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
        
        # Compute the minimal modular representation rank (mrr)
        mrr = compute_mrr(communication_matrix)
        
        total_metric_value += mrr
        instances_tested += 1
        
        if mrr > m * math.log(n):
            conjecture_holds = False
            counterexample = f"Seed {seed}: mrr={mrr} > O(m log n) for n={n}"
    
    return {
        "metric_name": "Minimal Modular Representation Rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def compute_mrr(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    
    # Gaussian elimination to find the rank of the matrix
    for i in range(m):
        if i < n:
            pivot_row = i
            while pivot_row < m and matrix[pivot_row][i] == 0:
                pivot_row += 1
            
            if pivot_row == m:
                continue
            
            # Swap rows to put a non-zero pivot in place
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            
            # Eliminate the pivot column
            for j in range(m):
                if i != j and matrix[j][i] != 0:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
            
            rank += 1
    
    return rank

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")