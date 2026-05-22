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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def boolean_function_to_permutation(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("f must be a list of length 2^n")
        return [f(i).index(1) for i in range(n)]
    
    def tensor_rank(permutation):
        n = len(permutation)
        rank = n
        for i in range(n):
            if permutation[i] == i:
                continue
            j = permutation[i]
            permutation[i], permutation[j] = permutation[j], permutation[i]
            rank -= 1
        return rank
    
    def minimal_representation_rank(f):
        n = int(math.log2(len(f)))
        matroid_matrix = [[0]*n for _ in range(n)]
        for i, x in enumerate(f):
            if x == 1:
                for j in range(n):
                    matroid_matrix[i%n][j] = (i//n) ^ (j//n)
        rank = n
        for i in range(n):
            if matroid_matrix[i][i] == 0:
                continue
            for j in range(n):
                if j != i and matroid_matrix[j][i] != 0:
                    for k in range(n):
                        matroid_matrix[j][k] ^= matroid_matrix[i][k]
                    rank -= 1
        return rank
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    
    try:
        permutation = boolean_function_to_permutation(f)
        tensor_rank_value = tensor_rank(permutation)
        representation_rank_value = minimal_representation_rank(f)
        
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": correlation_coefficient(tensor_rank_value, representation_rank_value),
            "instances_tested": 1,
            "conjecture_holds": correlation_coefficient(tensor_rank_value, representation_rank_value) >= 0.8,
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

def correlation_coefficient(x, y):
    n = len(x)
    if n != len(y):
        raise ValueError("x and y must have the same length")
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
    
    if denominator == 0:
        return None
    
    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(3, 157))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False and r["counterexample"] != "" for r in results):
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{' '.join(counterexamples)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")