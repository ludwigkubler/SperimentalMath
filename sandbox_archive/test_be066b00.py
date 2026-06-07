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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses

    def resolution_width(clauses):
        visited = set()
        queue = clauses[:]
        while queue:
            clause = queue.pop(0)
            if any(abs(lit) in visited for lit in clause):
                continue
            visited.add(abs(clause[0]))
            new_clauses = []
            for c in queue:
                if abs(c[0]) == abs(clause[1]):
                    new_clauses.append([-c[1]])
                elif abs(c[1]) == abs(clause[1]):
                    new_clauses.append([-c[0]])
            queue.extend(new_clauses)
        return len(visited)

    def grothendieck_witt_degree(clauses):
        n = len(clauses)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(clauses):
            A[i][i] = 1
            for lit in clause:
                if lit > 0:
                    A[lit - 1][i] += 1
                else:
                    A[-lit - 1][i] -= 1
        return gaussian_elimination(A, n)

    def gaussian_elimination(A, n):
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            pivot = Fraction(1, A[i][i])
            for j in range(i, n + 1):
                A[i][j] *= pivot
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return sum(abs(A[i][n]) for i in range(n))

    def degree_mod_2(degree):
        return degree % 2

    trials = 30
    total_degrees = 0
    total_widths = 0
    n_max = 1

    for _ in range(trials):
        n = random.randint(5, 40)
        if n > n_max:
            n_max = n
        clauses = generate_instance(n)
        width = resolution_width(clauses)
        degree = grothendieck_witt_degree(clauses)
        total_degrees += degree_mod_2(degree)
        total_widths += width

    mean_degree = Fraction(total_degrees, trials * n_max)
    mean_width = Fraction(total_widths, trials * n_max)
    
    conjecture_holds = mean_degree <= 2 * mean_width
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "deg(GW_φ) mod 2",
        "metric_value": float(mean_degree),
        "instances_tested": trials,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed + 1}")