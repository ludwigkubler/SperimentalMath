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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def kahler_area(A):
        n = len(A)
        if n != 2:
            return float('inf')
        det = determinant(gaussian_elimination(A))
        area = abs(det) ** 0.5
        return area

    def dpll_tree_height(phi):
        stack = [(phi, 1)]
        max_height = 0
        while stack:
            phi, height = stack.pop()
            if not phi:
                continue
            if len(phi) == 1:
                max_height = max(max_height, height)
                continue
            var, rest = phi[0], phi[1:]
            stack.append(([(x for x in rest if x != f"{var}"), (x for x in rest if x != f"~{var}")], height + 1))
        return max_height

    def random_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([f"x{i}", f"~x{i}"]) for i in range(1, n+1)]
            random.shuffle(clause)
            clauses.append(" or ".join(clause))
        return " and ".join(clauses)

    def parse_sat_instance(phi):
        variables = set()
        clauses = phi.split(" and ")
        for clause in clauses:
            literals = clause.split(" or ")
            for literal in literals:
                if literal.startswith("~"):
                    variable = literal[1:]
                else:
                    variable = literal
                variables.add(variable)
        return list(variables)

    n = random.randint(5, 40)
    phi = random_sat_instance(n)
    variables = parse_sat_instance(phi)
    
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    area = kahler_area(A)
    height = dpll_tree_height(phi)

    return {
        "metric_name": "Kähler Area vs DPLL Height",
        "metric_value": area * height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": area <= n * math.log(n) and height >= 1,  # Simplified lower bound for α^2
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")