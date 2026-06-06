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
    
    def generate_truth_table(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_minimal_order(truth_table):
        n = len(truth_table)
        variables = list(range(n))
        context = []
        for i in range(n):
            for j in range(i+1, n):
                if truth_table[i] != truth_table[j]:
                    context.append((i, j))
        return len(context) + 1
    
    def calculate_matrix_representation(truth_table):
        n = len(truth_table)
        matrix = [[truth_table[i * (2**(n-1)) + j] for j in range(2**(n-1))] for i in range(2)]
        return matrix
    
    def calculate_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            pivot_row = -1
            for row in range(m):
                if matrix[row][col] != 0:
                    if pivot_row == -1:
                        pivot_row = row
                    else:
                        # Swap rows to keep the pivot row at the top
                        matrix[pivot_row], matrix[row] = matrix[row], matrix[pivot_row]
                        for j in range(n):
                            matrix[row][j], matrix[pivot_row][j] = matrix[pivot_row][j], matrix[row][j]
                    break
            if pivot_row != -1:
                rank += 1
                # Eliminate other rows with non-zero entries in the current column
                for row in range(m):
                    if row != pivot_row and matrix[row][col] != 0:
                        factor = Fraction(matrix[row][col], matrix[pivot_row][col])
                        for j in range(n):
                            matrix[row][j] -= factor * matrix[pivot_row][j]
        return rank
    
    def calculate_ratio(truth_table):
        order = calculate_minimal_order(truth_table)
        matrix = calculate_matrix_representation(truth_table)
        rank = calculate_rank(matrix)
        if rank == 0:
            return None
        return Fraction(order, rank).limit_denominator()
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            truth_table = generate_truth_table(n)
            ratio = calculate_ratio(truth_table)
            if ratio is not None and ratio > 0:
                total_ratio += ratio
                instances_tested += 1
                n_max = max(n_max, n)
    
    mean_ratio = Fraction(total_ratio).limit_denominator() / instances_tested
    conjecture_holds = mean_ratio <= math.log2(n_max)
    counterexample = "" if conjecture_holds else f"Ratio: {mean_ratio}, Log(n): {math.log2(n_max)}"
    
    return {
        "metric_name": "Ratio of Minimal Order to Rank",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")