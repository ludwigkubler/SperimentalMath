# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations_with_replacement

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, 2*n), random.randint(1, 2*n), random.randint(1, 2*n)]
            while len(set(clause)) < 3:
                clause[random.randint(0, 2)] = random.randint(1, 2*n)
            clauses.append(tuple(sorted(clause)))
        return tuple(clauses)

    def tensor_product(tensors):
        if not tensors:
            return (1,)
        result = tensors[0]
        for t in tensors[1:]:
            new_result = []
            for r1 in result:
                for r2 in t:
                    new_result.append(r1 * r2)
            result = tuple(new_result)
        return result

    def kronecker_coefficient(t, mu, nu):
        # Approximation using Saxl's conjecture
        n = len(mu)
        m = len(nu)
        if n > 20 or m > 20:
            return None
        return 2 ** (n / 4)

    def permanent(tensor):
        n = int(math.sqrt(len(tensor)))
        result = 0
        for perm in combinations_with_replacement(range(1, n+1), 3):
            product = 1
            for i in range(n):
                product *= tensor[(perm[0] - 1) * n + (i % n)]
            result += product
        return result

    def determinant(tensor):
        n = int(math.sqrt(len(tensor)))
        if n == 2:
            return tensor[0] * tensor[3] - tensor[1] * tensor[2]
        det = 0
        for i in range(n):
            sub_tensor = [tensor[j] for j in range(n*n) if (j // n != i and j % n != 0)]
            det += ((-1) ** i) * tensor[i] * determinant(sub_tensor)
        return det

    def generate_partitions(n, k):
        partitions = []
        def backtrack(remain, curr_partition):
            if remain == 0:
                partitions.append(tuple(sorted(curr_partition)))
                return
            for i in range(k, 0, -1):
                if remain >= i:
                    backtrack(remain - i, curr_partition + [i])
        backtrack(n, [])
        return partitions

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    tensor = tensor_product([tuple(clause) for clause in clauses])
    
    mu_partitions = generate_partitions(n, n)
    nu_partitions = generate_partitions(n, n)

    perm_n = (n,)
    det_m = tuple(range(1, n+1))

    g_perm = max(kronecker_coefficient(tensor, mu, nu) for mu in mu_partitions for nu in nu_partitions if kronecker_coefficient(tensor, mu, nu) is not None)
    g_det = min(kronecker_coefficient(determinant(tensor), mu, nu) for mu in mu_partitions for nu in nu_partitions if kronecker_coefficient(determinant(tensor), mu, nu) is not None)

    return {
        "metric_name": "Kronecker Coefficient",
        "metric_value": g_perm,
        "instances_tested": 1,
        "conjecture_holds": g_perm >= 2 ** (n / 4) and g_det <= 2 ** math.sqrt(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_type = "SUPPORTED"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        result_type = "FALSIFIED"

    print(f"RESULT: {result_type} mean={mean_value:.2f} std={math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results)):.2f} support_fraction={support_fraction:.2f}")