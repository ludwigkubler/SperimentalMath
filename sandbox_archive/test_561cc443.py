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
    
    def generate_sat_instance(m, n):
        variables = set(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            pivot = -1
            for j in range(rank, m):
                if A[j][i] != 0:
                    pivot = j
                    break
            if pivot == -1:
                continue
            A[pivot], A[rank] = A[rank], A[pivot]
            for j in range(m):
                if i != j and A[j][i] != 0:
                    factor = A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def compute_minimal_representation(clauses, d):
        m = len(clauses)
        n = max(max(clause) for clause in clauses) + 1
        A = [[0] * (n + d) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                A[i][var] = 1
            A[i][-1] = -1
        rank = gaussian_elimination(A)
        return m - rank
    
    def compute_frege_proof_width(clauses):
        m = len(clauses)
        n = max(max(clause) for clause in clauses) + 1
        if m == 0:
            return 0
        if n == 0:
            return 0
        return m * (n - 1)
    
    def compute_measure(mu, d):
        return mu ** (d + 1)
    
    results = []
    for _ in range(30):
        m = random.randint(5, 40)
        n = random.randint(5, 40)
        d = random.randint(2, 5)
        clauses = generate_sat_instance(m, n)
        mu = compute_minimal_representation(clauses, d)
        frege_width = compute_frege_proof_width(clauses)
        measure = compute_measure(mu, d)
        if frege_width > measure:
            return {
                "metric_name": "Frege Proof Width",
                "metric_value": frege_width,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"m={m}, n={n}, d={d}"
            }
        results.append(frege_width)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([x for x in results if x <= compute_measure(mu, d)]) / len(results)
    
    return {
        "metric_name": "Frege Proof Width",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": n,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")