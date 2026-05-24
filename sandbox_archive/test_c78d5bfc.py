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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        A = [row[:] for row in A]
        r = gaussian_elimination(A)
        return sum(1 for row in r if any(row))
    
    def tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1 << (n - 1)):
            clause = [variables[i & ((1 << j) - 1)] for j in range(n)]
            if i & 1:
                clause.append(-variables[(i >> 1) & ((1 << (n - 2)) - 1)])
            clauses.append(clause)
        return variables, clauses
    
    def resolution_refutation_depth(clauses):
        stack = []
        while stack or clauses:
            if not stack:
                assignment = {var: random.choice([True, False]) for var in set(var for clause in clauses for var in clause)}
                res = [clause for clause in clauses if any(assignment[var] if var > 0 else not assignment[-var] for var in clause)]
                stack.append((res, {}))
            res, seen = stack.pop()
            if not res:
                return len(seen)
            unit_clause = next((c for c in res if len(c) == 1), None)
            if unit_clause is None:
                return float('inf')
            var = unit_clause[0]
            new_clauses = []
            for clause in res:
                if var not in clause and -var not in clause:
                    new_clauses.append(clause)
                elif var in clause:
                    new_clauses.extend([c + [-var] for c in clauses if -var not in c])
                else:
                    new_clauses.extend([c + [var] for c in clauses if var not in c])
            stack.append((new_clauses, seen | {var}))
        return float('inf')
    
    def quasigroup_representation(variables, clauses):
        n = len(variables)
        q = [[0] * (2 ** n) for _ in range(2 ** n)]
        for clause in clauses:
            for i in range(2 ** n):
                if all((i >> j & 1) == (var > 0 and assignment[var] or not assignment[-var]) for var in clause):
                    q[i][i] = 1
        return q
    
    def find_quasigroups(variables, clauses):
        n = len(variables)
        quasigroups = []
        for i in range(2 ** (n * n)):
            q = [[0] * (2 ** n) for _ in range(2 ** n)]
            for j in range(n):
                for k in range(n):
                    q[(i >> (j * n + k)) & 1][(i >> ((j + 1) * n + k)) & 1] = 1
            if rank(q) == n:
                quasigroups.append(q)
        return quasigroups
    
    variables, clauses = tseitin_formula(5)
    quasigroups = find_quasigroups(variables, clauses)
    
    min_rank = min(rank(q) for q in quasigroups)
    refutation_depth = resolution_refutation_depth(clauses)
    
    return {
        "metric_name": "ratio",
        "metric_value": refutation_depth / min_rank,
        "instances_tested": 1,
        "conjecture_holds": refutation_depth > math.exp(0.1 * math.log2(len(variables))),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
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
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")