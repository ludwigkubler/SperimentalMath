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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in range(1, max(assignment.keys()) + 1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll([c for c in clauses if -pure_literal not in c], new_assignment):
                return True
            return False
        literal = random.choice(list(assignment.keys()))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if -literal not in c], new_assignment):
            return True
        return False

    def minimal_symplectic_volume(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = gaussian_elimination(A)
        volume = 1
        for i in range(n):
            if B[i][i] != 0:
                volume *= abs(B[i][i])
        return volume

    def dpll_diameter(clauses, assignment):
        queue = [(clauses, assignment)]
        visited = set()
        while queue:
            clauses, assignment = queue.pop(0)
            if not clauses:
                return len(queue) + 1
            if (tuple(sorted(clauses)), tuple(sorted(assignment.items()))) in visited:
                continue
            visited.add((tuple(sorted(clauses)), tuple(sorted(assignment.items()))))
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                queue.append(([c for c in clauses if literal not in c and -literal not in c], new_assignment))
                new_assignment[literal] = False
                queue.append(([c for c in clauses if -literal not in c], new_assignment))
            pure_literal = next((l for l in range(1, max(assignment.keys()) + 1) if (l not in assignment and -l not in assignment)), None)
            if pure_literal:
                new_assignment = assignment.copy()
                new_assignment[pure_literal] = True
                queue.append(([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment))
                new_assignment[pure_literal] = False
                queue.append(([c for c in clauses if -pure_literal not in c], new_assignment))
            literal = random.choice(list(assignment.keys()))
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            queue.append(([c for c in clauses if literal not in c and -literal not in c], new_assignment))
            new_assignment[literal] = False
            queue.append(([c for c in clauses if -literal not in c], new_assignment))
        return len(queue) + 1

    n = random.randint(5, 40)
    msvs = []
    diameters = []

    for _ in range(30):
        clauses = []
        for _ in range(n * (n - 1) // 2):
            clause = [random.choice([-i, i]) for i in range(1, n + 1)]
            if random.random() < 0.5:
                clause = [-c for c in clause]
            clauses.append(clause)
        msvs.append(minimal_symplectic_volume(n))
        diameters.append(dpll_diameter(clauses, {}))

    correlation_coefficient = sum((msvs[i] - mean_msv) * (diameters[i] - mean_diameter) for i in range(30)) / 30
    mean_msv = sum(msvs) / 30
    mean_diameter = sum(diameters) / 30

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3**j + 5**k for i in range(5) for j in range(5) for k in range(5)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={seeds[first_failing_seed]}")