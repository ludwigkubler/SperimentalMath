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
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) for _ in range(random.randint(2, n))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return variables, clauses

    def tropical_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            pivot_row = None
            for j in range(i, m):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is not None:
                rank += 1
                for k in range(n):
                    matrix[i][k], matrix[pivot_row][k] = matrix[pivot_row][k], matrix[i][k]
                for j in range(m):
                    if j != i and matrix[j][i] != 0:
                        factor = -matrix[j][i] / matrix[i][i]
                        for k in range(n):
                            matrix[j][k] += factor * matrix[i][k]
        return rank

    def xor_and_tree_width(clauses):
        n = len(clauses)
        if n == 1:
            return 0
        width = float('inf')
        for i in range(1, 2**n):
            assignment = [bool((i >> j) & 1) for j in range(n)]
            unsatisfied = any(all(not (assignment[j-1] if c > 0 else not assignment[j-1]) for c in clause) for clause in clauses)
            if unsatisfied:
                width = min(width, sum(1 for bit in bin(i)[2:] if bit == '1'))
        return width

    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            variables, clauses = generate_cnf(n, int(n * (n - 1) / 2))
            matrix = [[-math.inf] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    for clause in clauses:
                        if i + 1 in clause and j + 1 in clause:
                            matrix[i][j] = max(matrix[i][j], -len(clause))
                            matrix[j][i] = max(matrix[j][i], -len(clause))
            rank = tropical_rank(matrix)
            width = xor_and_tree_width(clauses)
            ranks.append(rank)
            widths.append(width)

    correlation_coefficient = 0
    n_tested = len(ranks)
    if n_tested > 1:
        mean_r = sum(ranks) / n_tested
        mean_w = sum(widths) / n_tested
        variance_r = sum((x - mean_r) ** 2 for x in ranks) / (n_tested - 1)
        variance_w = sum((x - mean_w) ** 2 for x in widths) / (n_tested - 1)
        covariance = sum((ranks[i] - mean_r) * (widths[i] - mean_w) for i in range(n_tested)) / (n_tested - 1)
        correlation_coefficient = covariance / math.sqrt(variance_r * variance_w)

    conjecture_holds = correlation_coefficient > 0.8 and mean_w >= 3 * math.sqrt(variance_w)
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{cc}, mean_width=<{mw}>".format(cc=correlation_coefficient, mw=mean_w)

    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {" + ", ".join(f'"{k}": {v}' for k, v in result.items()) + "}")
        results.append(result)

    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean=%.4f std=%.4f support_fraction=%.2f" % (mean_r, std_r, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean=%.4f std=%.4f support_fraction=%.2f" % (mean_r, std_r, support_fraction))
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=%s first_failing_seed=%d" % ("correlation_coefficient=<{cc}, mean_width=<{mw}>".format(cc=r["metric_value"], mw=sum(r["instances_tested"] * [r["metric_value"]] for r in results) / sum(r["instances_tested"] for r in results)), first_failing_seed))