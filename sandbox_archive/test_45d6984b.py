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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i] for i in range(n)]

    def ehrhart_rank(phi):
        clauses = phi.split(' ')
        n = len(clauses)
        variables = set()
        for clause in clauses:
            if clause.startswith('-'):
                continue
            literals = clause.split(' ')[:-1]
            for literal in literals:
                variables.add(abs(int(literal)))
        m = len(variables)
        A = [[0] * (m + 1) for _ in range(m)]
        b = [0] * m
        for i, variable in enumerate(variables):
            for clause in clauses:
                if str(variable) in clause or '-' + str(variable) in clause:
                    A[i][variable - 1] += 1
                elif '-' + str(-variable) in clause:
                    A[i][variable - 1] -= 1
        return len(gaussian_elimination(A, b))

    def resolution_width(phi):
        clauses = phi.split(' ')
        n = len(clauses)
        variables = set()
        for clause in clauses:
            if clause.startswith('-'):
                continue
            literals = clause.split(' ')[:-1]
            for literal in literals:
                variables.add(abs(int(literal)))
        m = len(variables)
        width = 0
        queue = []
        while True:
            new_clause = None
            for i in range(n):
                if all(lit in queue or '-' + lit in queue for lit in clauses[i].split(' ')[:-1]):
                    new_clause = clauses[i]
                    break
            if not new_clause:
                break
            queue.append(new_clause)
            width = max(width, len([lit for lit in new_clause.split(' ')[:-1] if lit.startswith('-')]))
        return width

    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = []
            for i in range(n):
                if random.choice([True, False]):
                    clause.append(str(i + 1))
                else:
                    clause.append('-' + str(i + 1))
            cnf.append(' '.join(clause) + ' 0')
        return ' '.join(cnf)

    n_values = [5, 10, 15, 20, 30, 40]
    ehrhart_ranks = []
    widths = []

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = generate_cnf(n)
            ehrhart_ranks.append(ehrhart_rank(phi))
            widths.append(resolution_width(phi))

    if len(ehrhart_ranks) < 30 or len(widths) < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(ehrhart_ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }

    mean_ehrhart_rank = sum(ehrhart_ranks) / len(ehrhart_ranks)
    mean_width = sum(widths) / len(widths)
    correlation = 0
    for ehr, width in zip(ehrhart_ranks, widths):
        correlation += (ehr - mean_ehrhart_rank) * (width - mean_width)
    correlation /= math.sqrt(sum((ehr - mean_ehrhart_rank)**2 for ehr in ehrhart_ranks)) * math.sqrt(sum((width - mean_width)**2 for width in widths))

    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(ehrhart_ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8 and all(abs(ehr - width) <= 3 for ehr, width in zip(ehrhart_ranks, widths)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean_correlation = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_correlation} std=NOT_COMPUTABLE support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"Correlation does not meet threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")