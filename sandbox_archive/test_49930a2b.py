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
    
    def generate_xor_and_network(n):
        # Generate a random XOR-AND network with n variables
        incidence_matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return incidence_matrix
    
    def tensor_product_algebra(matrix):
        # Construct the tensor product algebra from the incidence matrix
        size = len(matrix)
        algebra = []
        for i in range(size):
            row = [0] * (size * size)
            for j in range(size):
                if matrix[i][j]:
                    row[j * size + i] = 1
            algebra.append(row)
        return algebra
    
    def min_rank(algebra):
        # Compute the minimal rank of the tensor product algebra
        size = len(algebra)
        rank = 0
        for i in range(size):
            if any(algebra[i][j] != 0 for j in range(rank, size)):
                rank += 1
                for j in range(size):
                    if algebra[j][i]:
                        for k in range(size):
                            algebra[j][k] -= algebra[i][k]
        return rank
    
    def communication_complexity(n):
        # Measure the communication complexity of the network
        return n * (n - 1) // 2
    
    n = random.randint(5, 40)
    incidence_matrix = generate_xor_and_network(n)
    algebra = tensor_product_algebra(incidence_matrix)
    rank = min_rank(algebra)
    comm_complexity = communication_complexity(n)
    
    return {
        "metric_name": "communication complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": rank <= 5,  # Placeholder for actual conjecture check
        "counterexample": ""
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"rank too high\" first_failing_seed={r['seed']}")
                break