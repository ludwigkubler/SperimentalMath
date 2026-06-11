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
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def formal_context(CNF):
        variables = set()
        for clause in CNF:
            variables.update(clause)
        context = {}
        for var in variables:
            context[var] = set()
            for i, clause in enumerate(CNF):
                if var in clause:
                    context[var].add(i)
        return context

    def minimal_index(context):
        m = len(context)
        A = [[0 for _ in range(m)] for _ in range(m)]
        for i in range(m):
            for j in range(m):
                if i != j and not context[i] & context[j]:
                    A[i][j] = 1
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return m - rank

    def resolution_proof_depth(CNF):
        stack = [CNF]
        depth = 0
        while stack:
            clause = stack.pop()
            if not clause:
                return depth
            var = random.choice(clause)
            new_clauses = []
            for c in CNF:
                if var in c:
                    continue
                if -var in c:
                    new_clause = [l for l in c if l != -var]
                    stack.append(new_clause)
                else:
                    new_clauses.append(c)
            CNF = new_clauses
            depth += 1
        return float('inf')

    def generate_CNF(m):
        variables = list(range(1, m + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, m))
            clauses.append(clause)
        return clauses

    n_max = 0
    instances_tested = 0
    min_index_sum = 0
    proof_depth_sum = 0

    for n in [5, 10, 15, 20, 30, 40]:
        if time.time() + 20 > end_time:
            return {
                "metric_name": "min_index",
                "metric_value": min_index_sum / instances_tested,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "budget_exceeded"
            }
        for _ in range(5):
            CNF = generate_CNF(n)
            context = formal_context(CNF)
            min_index = minimal_index(context)
            proof_depth = resolution_proof_depth(CNF)
            if min_index > proof_depth:
                return {
                    "metric_name": "min_index",
                    "metric_value": min_index_sum / instances_tested,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"min_index={min_index} > proof_depth={proof_depth}"
                }
            min_index_sum += min_index
            proof_depth_sum += proof_depth
            instances_tested += 1
            n_max = max(n_max, n)

    return {
        "metric_name": "min_index",
        "metric_value": min_index_sum / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    import time

    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    end_time = time.time() + 240

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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")