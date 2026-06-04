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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(cols):
                matrix[i][j] /= factor
            for j in range(rows):
                if i != j:
                    factor = Fraction(matrix[j][i])
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def is_independent(vectors):
        matrix = [list(v) for v in vectors]
        rank = len(gaussian_elimination(matrix))
        return rank == len(vectors)

    def tseitin_formula(n):
        variables = list(range(1, n+1))
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
            clauses.append([-i])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([i, -j])
                clauses.append([-i, j])
                clauses.append([i, j])
                clauses.append([-i, -j])
        return variables, clauses

    def dpll(clauses, assignment={}):
        if not clauses:
            return assignment
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment[literal] = literal.startswith("~")
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        pure_literal = next((l for l in range(1, 2*n+1) if (all(l not in c for c in clauses) or all(-l not in c for c in clauses))), None)
        if pure_literal:
            new_assignment[pure_literal] = True
            return dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment)
        literal = random.choice([l for l in range(1, 2*n+1) if l not in assignment and -l not in assignment])
        new_assignment[literal] = True
        result = dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        if result:
            return result
        new_assignment[literal] = False
        return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)

    def hecke_eigenvalues(clauses):
        n = len(clauses[0])
        variables, _ = tseitin_formula(n)
        vectors = []
        for i in range(1, 2*n+1):
            vector = [0] * (n-1)
            if i % 2 == 1:
                vector[(i-1)//2] = 1
            else:
                vector[(i-2)//2] = -1
            vectors.append(vector)
        independent_vectors = [v for v in vectors if is_independent(vectors + [v])]
        return len(independent_vectors)

    def resolution_width(clauses):
        assignment = {}
        stack = clauses[:]
        while stack:
            clause = stack.pop()
            unit_clause = next((c for c in clause if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment[literal] = literal.startswith("~")
                return len(new_assignment)
            pure_literal = next((l for l in range(1, 2*n+1) if (all(l not in c for c in stack) or all(-l not in c for c in stack))), None)
            if pure_literal:
                new_assignment[pure_literal] = True
                return len(new_assignment)
            literal = random.choice([l for l in range(1, 2*n+1) if l not in assignment and -l not in assignment])
            new_assignment[literal] = True
            stack.extend([c for c in clauses if literal not in c and -literal not in c])
        return len(new_assignment)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        N = hecke_eigenvalues(clauses)
        w = resolution_width(clauses)
        results.append((N, w))

    if not results:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    N_values, w_values = zip(*results)
    correlation_coefficient = sum((N - mean_N) * (w - mean_w) for N, w in results) / len(results)
    mean_N = sum(N_values) / len(N_values)
    mean_w = sum(w_values) / len(w_values)
    std_dev = math.sqrt(sum((w - mean_w)**2 for w in w_values) / len(w_values))
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_w <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")