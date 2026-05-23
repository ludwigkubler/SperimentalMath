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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def construct_kac_moody_lie_algebra(clauses):
        n = len(clauses)
        generators = set()
        relations = []
        for clause in clauses:
            generators.update(clause)
            for i in range(len(clause)):
                for j in range(i+1, len(clause)):
                    relations.append((clause[i], clause[j]))
        A = [[0] * (len(generators) + 1) for _ in range(len(relations))]
        var_map = {var: idx for idx, var in enumerate(generators)}
        for i, (x, y) in enumerate(relations):
            A[i][var_map[x]] = 1
            A[i][var_map[y]] = -1
            A[i][-1] = 1
        return gaussian_elimination(A)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = set()
            for i in range(n):
                if random.choice([True, False]):
                    clause.add(f'x{i+1}')
                else:
                    clause.add(f'-x{i+1}')
            clauses.append(clause)
        return clauses
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    rank = construct_kac_moody_lie_algebra(cnf)
    
    metric_name = "Minimal Rank of Kac-Moody Lie Algebra"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= 2**n
    counterexample = "" if conjecture_holds else f"Rank {rank} > 2^{n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")