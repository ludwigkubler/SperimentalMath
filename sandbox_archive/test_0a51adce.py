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
            max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(1, matrix[i][i])
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = -matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] += factor * matrix[i][j]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        row_echelon_form = gaussian_elimination(matrix)
        rank = 0
        for i in range(rows):
            if any(row_echelon_form[i]):
                rank += 1
        return rank

    def resolution_width(cnf):
        # Simplified DPLL algorithm to compute resolution width
        clauses = [set(clause) for clause in cnf]
        queue = []
        while True:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                return len(queue)
            literal, = unit_clause
            queue.append(literal)
            new_clauses = set()
            for clause in clauses:
                if literal in clause:
                    continue
                if -literal in clause:
                    return len(queue)
                new_clauses.add(clause ^ {literal})
            clauses.update(new_clauses)

    def generate_cnf(num_vars, num_clauses):
        cnf = []
        literals = list(range(1, num_vars + 1)) + [-i for i in range(1, num_vars + 1)]
        for _ in range(num_clauses):
            clause = random.sample(literals, random.randint(2, 3))
            cnf.append(clause)
        return cnf

    n_max = 40
    instances_tested = 0
    total_rank = 0
    total_width = 0

    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2 * n, 4 * n))
            rank_value = rank(cnf)
            width_value = resolution_width(cnf)
            total_rank += rank_value
            total_width += width_value
            instances_tested += 1

    if instances_tested < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }

    mean_rank = total_rank / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(rank_value * width_value for rank_value, width_value in zip(cnf_ranks, cnf_widths)) - 
                               mean_rank * sum(cnf_widths) - mean_width * sum(cnf_ranks)) / math.sqrt(
        instances_tested * sum((rank_value - mean_rank) ** 2 for rank_value in cnf_ranks) * 
                              instances_tested * sum((width_value - mean_width) ** 2 for width_value in cnf_widths))

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(0.5 <= coeff < 1 for coeff in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + \
             [31, 37, 41, 43, 47, 53, 59, 61, 67, 71] + \
             [73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results and result["metric_value"] >= 0.5):
        print("RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")