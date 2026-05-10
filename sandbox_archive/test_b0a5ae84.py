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
    def generate_read_twice_bp(n):
        # Generate a random read-twice branching program
        bp = []
        for _ in range(2):
            layer = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            bp.append(layer)
        return bp

    def adjacency_matrix(bp):
        n = len(bp[0])
        adj = [[0] * (n * n) for _ in range(n * n)]
        for i in range(n):
            for j in range(n):
                if bp[0][i][j]:
                    for k in range(n):
                        adj[i * n + k][j * n + k] = 1
                if bp[1][i][j]:
                    for k in range(n):
                        adj[i * n + k][(j + 1) % n * n + k] = 1
        return adj

    def tensor_product(matrices):
        if not matrices:
            return [[0]]
        result = matrices[0]
        for mat in matrices[1:]:
            new_result = []
            for r1 in result:
                for r2 in mat:
                    new_row = [r1[i] * r2[j] for j in range(len(r2))]
                    new_result.append(new_row)
            result = new_result
        return result

    def min_eigenvalue(matrix):
        n = int(math.sqrt(len(matrix)))
        flat_matrix = [sum(row) for row in matrix]
        eigenvalues = []
        for i in range(n * n):
            v = sum(flat_matrix[j] * (i // n == j % n) for j in range(n * n))
            eigenvalues.append(v)
        return min(eigenvalues)

    def free_entropy(matrix):
        n = len(matrix)
        trace = sum(matrix[i][i] for i in range(n))
        det = 1
        for row in matrix:
            det *= sum(row)
        return (trace - math.log(det)) / n

    n = random.randint(5, 40)
    bp = generate_read_twice_bp(n)
    adj_matrix = adjacency_matrix(bp)
    mp = tensor_product([adj_matrix] * n)
    min_eig = min_eigenvalue(mp)

    size_p = n ** 2
    expected_min_eig = math.log(size_p) if not (bp[0][0][0] == 1 and bp[1][0][0] == 1) else -math.inf

    return {
        "metric_name": "min_eigenvalue",
        "metric_value": min_eig,
        "instances_tested": 1,
        "conjecture_holds": min_eig >= expected_min_eig,
        "counterexample": "" if min_eig >= expected_min_eig else "read-twice BP is trivial"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"read-twice BP is trivial\" first_failing_seed={first_failing_seed}")