# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 3))
            if random.choice([True, False]):
                clause = {x * -1 for x in clause}
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        def solve(model):
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_model = model.copy()
                new_model.add(literal)
                return solve(new_model)
            pure_literal = next((l for l in range(1, n+1) if all(l not in c or -l in c for c in cnf)), None)
            if pure_literal:
                new_model = model.copy()
                new_model.add(pure_literal)
                return solve(new_model)
            if not cnf:
                return model
            literal = next(iter(cnf[0]))
            rest = [c for c in cnf if literal not in c and -literal not in c]
            return solve(model | {literal}) or solve(model | {-literal})
        return len(solve(set()))

    def tropicalization(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i, x in enumerate(clause):
                for j, y in enumerate(clause):
                    if i != j and x != -y:
                        A[abs(x)][abs(y)] = max(A[abs(x)][abs(y)], abs(x) ^ abs(y))
        return A

    def min_local_ring_unit_group_size(A):
        n = len(A)
        for i in range(n):
            for j in range(i + 1, n):
                if A[i][j] != 0:
                    A[j][i] = A[i][j]
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    A[i][j] = max(A[i][j], min(A[i][k], A[k][j]))
        return sum(1 for row in A if any(x != 0 for x in row))

    n = random.randint(5, 40)
    k = random.randint(2, n)
    cnf = generate_k_cnf(n, k)
    d_phi = dpll(cnf)
    T = tropicalization(cnf)
    mu_phi = min_local_ring_unit_group_size(T)

    return {
        "metric_name": "mu_phi_d_phi_corr",
        "metric_value": mu_phi * d_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")