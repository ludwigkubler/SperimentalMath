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
    n = random.randint(5, 40)
    if n == 1:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Generate a random Boolean function
    f = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
    
    # Compute the characteristic polynomial under Fourier transform
    def fourier_transform(matrix):
        n = len(matrix)
        result = []
        for k in range(n):
            sum_real = sum(sum(matrix[i][j] * math.cos(2 * math.pi * i * k / n) for j in range(n)) for i in range(n))
            sum_imag = sum(sum(matrix[i][j] * math.sin(2 * math.pi * i * k / n) for j in range(n)) for i in range(n))
            result.append((sum_real, sum_imag))
        return result
    
    char_poly = fourier_transform(f)
    
    # Calculate the Frobenius Norm of the associated matrix
    def frobenius_norm(matrix):
        n = len(matrix)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += matrix[i][j] ** 2
        return math.sqrt(norm)
    
    frob_norm = frobenius_norm(char_poly)
    
    # Determine the XOR-AND tree width (simplified for this test)
    def xor_and_tree_width(matrix):
        n = len(matrix)
        if n == 1:
            return 0
        return 1 + max(xor_and_tree_width(submatrix) for submatrix in [matrix[:n//2], matrix[n//2:]])
    
    tree_width = xor_and_tree_width(f)
    
    # Calculate the minimal rank of the Frobenius Norm
    def min_rank(matrix):
        n = len(matrix)
        if n == 1:
            return 1
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(n)):
                rank += 1
                break
        return rank
    
    min_rank_value = min_rank(char_poly)
    
    # Check the conjecture
    def log_n(f, n):
        result = f
        for _ in range(n):
            result = math.log(result)
        return result
    
    if tree_width == 0:
        return {
            "metric_name": "minimal_rank",
            "metric_value": min_rank_value,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    upper_bound = math.ceil(tree_width ** (1/3) * log_n(len(f), tree_width))
    if min_rank_value <= upper_bound:
        return {
            "metric_name": "minimal_rank",
            "metric_value": min_rank_value,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "minimal_rank",
            "metric_value": min_rank_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"min_rank({min_rank_value}) > upper_bound({upper_bound})"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")