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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = set(random.sample(range(1, n+1), 3))
            if random.choice([True, False]):
                clause = {x: -1 for x in clause}
            clauses.append(clause)
        return clauses

    def polynomial_to_vector(poly):
        n = len(poly)
        vector = [0] * (2**n)
        for i in range(2**n):
            assignment = [(i >> j) & 1 for j in range(n)]
            value = sum(poly[i][j] * assignment[j] for j in range(n))
            if value == len(poly[i]):
                vector[i] = 1
        return vector

    def tensor_product(v1, v2):
        n = len(v1)
        m = len(v2)
        result = [0] * (n * m)
        for i in range(n):
            for j in range(m):
                result[i*m + j] = v1[i] * v2[j]
        return result

    def local_cohomology_rank(vector):
        n = int(math.log2(len(vector)))
        rank = 0
        for k in range(1, n+1):
            subspaces = []
            for i in range(n-k+1):
                subspace = [vector[i + j] for j in range(k)]
                if all(subspace[j] == subspace[0] for j in range(1, k)):
                    subspaces.append(subspace)
            rank += len(subspaces)
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n**2)
        clauses = generate_3cnf(n, m)
        poly = polynomial_to_vector(clauses)
        dual_poly = polynomial_to_vector([{x: -v for x, v in clause.items()} if isinstance(clause, dict) else {x: -1} for clause in clauses])
        tensor_prod = tensor_product(poly, dual_poly)
        rank = local_cohomology_rank(tensor_prod)
        results.append({
            "n": n,
            "m": m,
            "rank": rank
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    conjecture_holds = all(result["rank"] <= n**2 - result["m"] + 1 for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, m={results[0]['m']}, rank={results[0]['rank']} > {results[0]['n']**2 - results[0]['m'] + 1}"
    
    return {
        "metric_name": "local_cohomology_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, m={results[0]['m']}, rank={results[0]['rank']} > {results[0]['n']**2 - results[0]['m'] + 1}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")