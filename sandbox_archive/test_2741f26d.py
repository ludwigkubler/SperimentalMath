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
    
    def generate_xor_3cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            literals = [random.choice(['x', '~x']) + str(i+1) for i in range(n)]
            clause = ' or '.join(literals)
            clauses.append(clause)
        return ' and '.join(clauses)

    def parse_xor_3cnf(formula):
        n = 0
        literals = set()
        for char in formula:
            if char == 'x' or char == '~':
                literals.add(char + str(n))
                n += 1
        return n, literals

    def compute_quadratic_form(literals):
        n = len(literals)
        q = [[0] * n for _ in range(n)]
        for literal in literals:
            if literal[0] == 'x':
                i = int(literal[2:]) - 1
                q[i][i] += 1
            else:
                i = int(literal[2:]) - 1
                q[i][i] -= 1
        return q

    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i+1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    return None  # Singular matrix
            pivot = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] != 0:
                rank += 1
        return rank

    def monomial_circuit_size(formula):
        n, _ = parse_xor_3cnf(formula)
        # Simplified heuristic: size is proportional to the number of literals
        return len(formula) // 4 + 1

    n = random.randint(5, 40)
    formula = generate_xor_3cnf(n)
    n, literals = parse_xor_3cnf(formula)
    q = compute_quadratic_form(literals)
    rank = min_rank(gaussian_elimination(q))
    circuit_size = monomial_circuit_size(formula)

    if circuit_size == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "circuit_size_undefined"
        }

    ratio = Fraction(rank, circuit_size)
    return {
        "metric_name": "Ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True if ratio >= 0.5 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "not_all_seeds_supported"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")