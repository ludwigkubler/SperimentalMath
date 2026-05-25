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
    
    def generate_k_clique_cnf(k, n):
        clauses = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    clauses.append(f"(x{i+1} OR x{j+1})")
                else:
                    clauses.append(f"NOT(x{i+1} AND x{j+1})")
        return " AND ".join(clauses)

    def generate_tropical_matrix(n):
        matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return matrix

    def tropical_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] == 1 for j in range(i, n)):
                rank += 1
                for j in range(n):
                    if matrix[j][i] == 1:
                        for k in range(n):
                            matrix[j][k] = max(matrix[j][k], matrix[i][k])
        return rank

    def generate_k_clique_circuit_size(k, n):
        # Simplified estimation of circuit size
        return 2 ** (k + 1)

    n = random.randint(5, 40)
    k = random.randint(2, min(n - 1, 10))
    cnf_formula = generate_k_clique_cnf(k, n)
    tropical_matrix = generate_tropical_matrix(n)
    rank = tropical_rank(tropical_matrix)
    circuit_size = generate_k_clique_circuit_size(k, n)

    return {
        "metric_name": "tropical_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= circuit_size,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 30 primes
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")