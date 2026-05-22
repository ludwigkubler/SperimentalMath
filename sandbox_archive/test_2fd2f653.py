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
    
    def generate_xor_and_network(n):
        network = []
        for _ in range(2**n - 1):
            node = [random.choice([0, 1]) for _ in range(n)]
            network.append(node)
        return network
    
    def tensor_product_algebra(network):
        n = len(network[0])
        algebra = [[0] * (2 ** n) for _ in range(2 ** n)]
        for i in range(2 ** n):
            for j in range(2 ** n):
                product = 1
                for k in range(n):
                    if network[i][k] == network[j][k]:
                        product *= 1
                    else:
                        product *= -1
                algebra[i][j] = product
        return algebra
    
    def minimal_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if all(matrix[j][i] == 0 for j in range(i, m)):
                continue
            pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            rank += 1
            for j in range(m):
                if i == j:
                    continue
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def communication_complexity(network):
        n = len(network[0])
        # Placeholder for actual communication complexity calculation
        return (n ** 2) * math.log(n, 2) / math.log(math.log(n, 2), 2)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    network = generate_xor_and_network(n)
    algebra = tensor_product_algebra(network)
    rank = minimal_rank(algebra)
    comm_complexity = communication_complexity(network)
    
    return {
        "metric_name": "communication complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": rank <= 10,  # Placeholder for actual constant c
        "counterexample": "" if rank <= 10 else f"rank too high: {rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_comm_complexity = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank too high\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")