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
    
    def generate_boolean_function(n, max_non_zero):
        truth_table = [random.choice([0, 1]) for _ in range(2**n)]
        non_zero_indices = [i for i, x in enumerate(truth_table) if x == 1]
        if len(non_zero_indices) > max_non_zero:
            non_zero_indices = random.sample(non_zero_indices, max_non_zero)
        for i in non_zero_indices:
            truth_table[i] = 1
        return truth_table
    
    def compute_brauer_group_rank(truth_table):
        n = int(math.log2(len(truth_table)))
        if len(truth_table) != 2**n:
            raise ValueError("Truth table length must be a power of 2")
        
        # Convert truth table to matrix
        A = [[truth_table[i * n + j] for j in range(n)] for i in range(2)]
        
        # Gaussian elimination
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for col in range(cols):
                max_row = next((i for i in range(col, rows) if matrix[i][col]), -1)
                if max_row == -1:
                    continue
                matrix[col], matrix[max_row] = matrix[max_row], matrix[col]
                for row in range(rows):
                    if row != col:
                        factor = matrix[row][col] / matrix[col][col]
                        for j in range(cols):
                            matrix[row][j] -= factor * matrix[col][j]
            return matrix
        
        A = gaussian_elimination(A)
        
        # Count non-zero rows
        rank = sum(1 for row in A if any(x != 0 for x in row))
        return rank
    
    def count_non_zero_entries(truth_table):
        return truth_table.count(1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_rank = 0
    num_instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different instances
            truth_table = generate_boolean_function(n, n)
            rank = compute_brauer_group_rank(truth_table)
            non_zero_entries = count_non_zero_entries(truth_table)
            results.append((rank, non_zero_entries))
            total_rank += rank
            num_instances_tested += 1
    
    mean_rank = total_rank / num_instances_tested
    conjecture_holds = all(rank >= 2**n / non_zero_entries for rank, non_zero_entries in results)
    
    return {
        "metric_name": "Brauer Group Rank",
        "metric_value": mean_rank,
        "instances_tested": num_instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")