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

def generate_instance(n):
    num_clauses = random.randint(2, n)
    phi = []
    for _ in range(num_clauses):
        clause_length = random.randint(1, n)
        clause = set()
        while len(clause) < clause_length:
            var = random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)
            clause.add(var)
        phi.append(' '.join(str(v) for v in sorted(clause)))
    return ' '.join(phi)

def tseitin_formula(phi):
    literals = set()
    clauses = phi.split()
    new_vars = {}
    new_clause_count = 0

    def get_new_var():
        nonlocal new_clause_count
        new_clause_count += 1
        return f'x{new_clause_count}'

    for clause in clauses:
        literal = clause[0]
        literals.add(literal)
        if literal.startswith('-'):
            negated_literal = literal[1:]
        else:
            negated_literal = '-' + literal

        if literal not in new_vars:
            new_var = get_new_var()
            new_vars[literal] = new_var
            new_vars[negated_literal] = '-' + new_var
            phi += f'{new_var} {negated_literal} 0'
        else:
            phi += f'{new_vars[literal]} {negated_literal} 0'

    return phi

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find a pivot
        if matrix[i][i] == 0:
            for j in range(i + 1, rows):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                return None  # Pivot is zero, no solution

        # Normalize the pivot row
        pivot = matrix[i][i]
        for j in range(cols):
            matrix[i][j] /= pivot

        # Eliminate other rows
        for j in range(rows):
            if i != j:
                factor = matrix[j][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]

    return matrix

def homology_group_order(matrix):
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def resolution_width(phi):
    clauses = phi.split()
    max_width = 0
    for clause in clauses:
        width = len(clause.split())
        if width > max_width:
            max_width = width
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []

    for n in n_values:
        phi = generate_instance(n)
        phi_tseitin = tseitin_formula(phi)
        matrix = []
        for clause in phi_tseitin.split():
            row = [int(lit) if lit.startswith('-') else -int(lit) for lit in clause.split()]
            matrix.append(row)

        homology_order = homology_group_order(matrix)
        width = resolution_width(phi_tseitin)
        results.append({
            "n": n,
            "homology_order": homology_order,
            "width": width
        })

    if not results:
        return {
            "metric_name": "Homology Order vs Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }

    homology_orders = [r["homology_order"] for r in results]
    widths = [r["width"] for r in results]

    if any(h > 1.5 * w for h, w in zip(homology_orders, widths)):
        return {
            "metric_name": "Homology Order vs Width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "homology_order > 1.5 * width"
        }

    correlation = sum((h - mean_h) * (w - mean_w) for h, w in zip(homology_orders, widths)) / len(results)
    mean_h = sum(homology_orders) / len(homology_orders)
    mean_w = sum(widths) / len(widths)

    return {
        "metric_name": "Homology Order vs Width",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    correlation_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    instances_tested = sum(r["instances_tested"] for r in results)
    n_max = max(r["n_max"] for r in results)

    if all(correlation is not None and abs(correlation) > 0.7 for correlation in correlation_values):
        support_fraction = len([r for r in results if r["metric_value"] is not None]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(correlation_values)/len(correlation_values):.2f} std={math.sqrt(sum((x - sum(correlation_values)/len(correlation_values))**2 for x in correlation_values) / len(correlation_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(correlation is not None and abs(correlation) <= 0.7 for correlation in correlation_values):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["metric_value"] is not None and abs(result["metric_value"]) <= 0.7)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_data")