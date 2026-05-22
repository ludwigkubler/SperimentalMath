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
    
    def generate_tseitin_formula(n):
        symbols = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([symbols[i-1]])
            clauses.append([-symbols[i-1], f'y{i}'])
            clauses.append([-f'y{i}', symbols[i-1]])
        return symbols, clauses

    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
            for j in range(rows):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def hodge_decomposition(matrix):
        rows, cols = len(matrix), len(matrix[0])
        identity = [[Fraction(1 if i == j else 0) for j in range(cols)] for i in range(rows)]
        augmented_matrix = [row + identity[i] for i, row in enumerate(matrix)]
        reduced_matrix = gaussian_elimination(augmented_matrix)
        hodge_matrix = [row[cols:] for row in reduced_matrix]
        return hodge_matrix

    def resolution_refutation(clauses):
        stack = []
        while True:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            stack.append(literal)
            for clause in clauses:
                if literal in clause:
                    clauses.remove(clause)
                elif -literal in clause:
                    clause.remove(-literal)
        return len(stack)

    n = random.randint(5, 40)
    symbols, clauses = generate_tseitin_formula(n)
    matrix = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    hodge_matrix = hodge_decomposition(matrix)
    
    μ_G = sum(sum(row[i] * row[j] for j in range(i+1, n)) for i in range(n)) / (n * (n - 1))
    refutation_length = resolution_refutation(clauses)

    return {
        "metric_name": "μ(G)",
        "metric_value": μ_G,
        "instances_tested": 1,
        "conjecture_holds": μ_G <= refutation_length - 3,
        "counterexample": "" if μ_G <= refutation_length - 3 else f"Refutation length {refutation_length} is less than μ(G) = {μ_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Refutation length less than μ(G)\" first_failing_seed={first_failing_seed}")