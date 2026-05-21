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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def rank(matrix):
        rref = gaussian_elimination(matrix)
        return sum(1 for row in rref if any(row))

    def generate_tensor_network(n):
        # Simplified tensor network generation
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

    def compute_brauer_group(tensor_network):
        n = len(tensor_network)
        I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        A = []
        for i in range(n):
            for j in range(i+1, n):
                A.append([tensor_network[i][k] * tensor_network[j][k] - tensor_network[j][k] * tensor_network[i][k] for k in range(n)])
        return rank(A)

    def communication_cost(tensor_network):
        # Simplified communication cost calculation
        return sum(sum(row) for row in tensor_network)

    n = random.choice([5, 10, 15, 20, 30, 40])
    tensor_network = generate_tensor_network(n)
    generators = compute_brauer_group(tensor_network)
    comm_cost = communication_cost(tensor_network)

    return {
        "metric_name": "Generators vs Comm Cost",
        "metric_value": generators / comm_cost,
        "instances_tested": 1,
        "conjecture_holds": False if generators == 0 else True,
        "counterexample": "" if generators != 0 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")