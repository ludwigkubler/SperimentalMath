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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 0
        mid = n // 2
        left = f[:mid]
        right = f[mid:]
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    
    def real_algebraic_lattice_rank(f):
        n = len(f)
        if n == 1:
            return 1
        mid = n // 2
        left = f[:mid]
        right = f[mid:]
        rank_left = real_algebraic_lattice_rank(left)
        rank_right = real_algebraic_lattice_rank(right)
        return max(rank_left, rank_right) + 1
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i+1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None  # Singular matrix
            for j in range(m):
                if j == i:
                    continue
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(i, m):
                    matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def minimal_rank(f):
        n = len(f)
        if n == 1:
            return 1
        mid = n // 2
        left = f[:mid]
        right = f[mid:]
        rank_left = minimal_rank(left)
        rank_right = minimal_rank(right)
        matrix = []
        for i in range(2**mid):
            row = [left[i], right[i]]
            matrix.append(row)
        return gaussian_elimination(matrix)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        xor_and_width = xor_and_tree_width(f)
        lattice_rank = minimal_rank(f)
        if lattice_rank is None:
            continue
        results.append((xor_and_width, lattice_rank))
    
    if not results:
        return {
            "metric_name": "XOR-AND Tree Width vs. Lattice Rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    xor_and_widths, lattice_ranks = zip(*results)
    mean_xor_and_width = sum(xor_and_widths) / len(xor_and_widths)
    std_xor_and_width = math.sqrt(sum((x - mean_xor_and_width)**2 for x in xor_and_widths) / len(xor_and_widths))
    
    if any(xor_and_width > 1.1 * lattice_rank for xor_and_width, lattice_rank in results):
        return {
            "metric_name": "XOR-AND Tree Width vs. Lattice Rank",
            "metric_value": mean_xor_and_width,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "Found a counterexample where XOR-AND tree width exceeds 10% of lattice rank"
        }
    
    return {
        "metric_name": "XOR-AND Tree Width vs. Lattice Rank",
        "metric_value": mean_xor_and_width,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")