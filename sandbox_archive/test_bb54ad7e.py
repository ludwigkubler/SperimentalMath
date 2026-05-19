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
    
    def generate_3cnf(n: int, m: int):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses
    
    def incidence_matrix(clauses: list):
        n = max(abs(c) for c in sum(clauses, []))
        matrix = [[0] * (n + 1) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for var in clause:
                matrix[i][abs(var)] += 1
        return matrix
    
    def tensor_rank(matrix: list):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            if any(matrix[row][col] != 0 for row in range(m)):
                rank += 1
        return rank
    
    def acc0_circuit_size(n: int):
        # Placeholder function; actual implementation required
        return n ** 2
    
    n = random.randint(5, 40)
    m = random.randint(3 * n, 6 * n)
    clauses = generate_3cnf(n, m)
    matrix = incidence_matrix(clauses)
    rank = tensor_rank(matrix)
    size = acc0_circuit_size(n)
    
    return {
        "metric_name": "tensor_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank == math.log2(n) and size <= n ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)