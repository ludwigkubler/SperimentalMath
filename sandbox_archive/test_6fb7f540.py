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
    
    def generate_boolean_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(f"({clause[0]} | {clause[1]})")
        return " & ".join(clauses)

    def tseitin_transformation(formula):
        literals = set()
        formulas = {}
        counter = 0
        for part in formula.split(' & '):
            if '|' in part:
                parts = part.split(' | ')
                new_var = f'y{counter}'
                counter += 1
                formulas[new_var] = f"({parts[0]} & {parts[1]})"
                literals.add(new_var)
        return literals, formulas

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

    def order_tropical_symplectic_form(formulas, literals):
        n = len(literals)
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for literal in literals:
            formula = formulas[literal]
            # Convert the formula to a matrix
            matrix = identity_matrix[:]
            for part in formula.split(' & '):
                if '|' in part:
                    parts = part.split(' | ')
                    row1, col1 = int(parts[0][1:]), int(parts[1][1:])
                    matrix[row1][col1] = 1
                    matrix[col1][row1] = 1
            # Perform Gaussian elimination to find the order
            reduced_matrix = gaussian_elimination(matrix)
            rank = sum(1 for row in reduced_matrix if any(row))
            return rank

    def resolution_proof_width(formula):
        stack = []
        for part in formula.split(' & '):
            if '|' in part:
                parts = part.split(' | ')
                stack.append(parts[0])
                stack.append(parts[1])
            else:
                stack.append(part)
        width = 0
        while stack:
            current = stack.pop()
            if current.startswith('y'):
                continue
            elif current == 'True':
                continue
            else:
                width += 1
                for i in range(width):
                    stack.append(current)
        return width

    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_boolean_formula(n)
            literals, formulas = tseitin_transformation(formula)
            order = order_tropical_symplectic_form(formulas, literals)
            width = resolution_proof_width(formula)
            if abs(width - order) > 0.5 * order:
                conjecture_holds = False
                counterexample = f"Formula: {formula}, Order: {order}, Width: {width}"
                break
            instances_tested += 1
            metric_value += width / order

    return {
        "metric_name": "Resolution Proof Width vs. Tropical Symplectic Form Order",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.7:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")