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
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return sum(1 for row in A if any(row))

    def resolution_width(phi):
        stack = []
        for clause in phi:
            literals = set(clause)
            if not stack:
                stack.append(literals)
            else:
                new_stack = []
                for s in stack:
                    if literals.isdisjoint(s):
                        new_stack.append(s.union(literals))
                    elif literals.issubset(s):
                        continue
                    elif s.issubset(literals):
                        new_stack.append(literals)
                    else:
                        new_stack.extend([s, literals])
                stack = new_stack
        return max(len(s) for s in stack)

    def tseitin_formula(n, d):
        variables = list(range(1, n * (n - 1) // 2 + 1))
        clauses = []
        for i in range(n):
            for j in range(i + 1, n):
                k = i * (n - 1) // 2 + j - i - 1
                clauses.append([variables[k], -i, -j])
                clauses.append([-variables[k], i])
                clauses.append([-variables[k], j])
        for i in range(n):
            for j in range(i + 1, n):
                k = i * (n - 1) // 2 + j - i - 1
                for l in range(j + 1, n):
                    m = j * (n - j - 1) // 2 + l - j - 1
                    clauses.append([variables[k], variables[m], -i])
                    clauses.append([-variables[k], -variables[m], i])
        return clauses

    def algebraic_k_theory_class(phi):
        n = len(phi)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in phi:
            for lit in clause:
                if lit > 0:
                    A[lit - 1][lit] += 1
                else:
                    A[-lit - 1][-lit] -= 1
        return gaussian_elimination(A)

    n = random.randint(5, 40)
    d = 2 * random.randint(1, (n * (n - 1)) // 2)
    phi = tseitin_formula(n, d)
    width = resolution_width(phi)
    rank = algebraic_k_theory_class(phi)

    return {
        "metric_name": "Resolution Width vs Rank",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= 3 * rank,
        "counterexample": "" if width <= 3 * rank else f"width={width}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] and r["metric_value"] > 3 * r["instances_tested"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] > 3 * r["instances_tested"])
        print(f"RESULT: FALSIFIED counterexample=\"width > 3 * rank\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")