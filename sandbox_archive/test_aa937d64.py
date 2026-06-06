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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(i, cols):
                matrix[i][j] /= pivot
            for k in range(rows):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def resolution_width(cnf):
        queue = cnf[:]
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(len(queue)):
                    if len(set(queue[i]) & set(queue[j])) == 2:
                        new_clause = [x for x in queue[i] if x not in queue[j]] + [x for x in queue[j] if -x not in queue[i]]
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return len(queue)
            queue.append(new_clause)
    
    def monodromy_group(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            if len(clause) == 2 and abs(clause[0]) != abs(clause[1]):
                i, j = abs(clause[0]), abs(clause[1])
                matrix[i][j] += 1
                matrix[j][i] += 1
        matrix = gaussian_elimination(matrix)
        order = 1
        for row in matrix:
            if sum(row) != 0:
                order *= sum(row)
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_order = 0
    total_width = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
            order = monodromy_group(cnf)
            width = resolution_width(cnf)
            total_order += order
            total_width += width
            instances_tested += 1
            max_n = max(max_n, n)
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    
    correlation = (instances_tested * sum(order * width for order, width in zip([mean_order] * instances_tested, [mean_width] * instances_tested)) -
                   sum(mean_order) * sum(mean_width)) / math.sqrt((instances_tested * sum(order ** 2 for order in [mean_order] * instances_tested) - sum(mean_order) ** 2) *
                                                                 (instances_tested * sum(width ** 2 for width in [mean_width] * instances_tested) - sum(mean_width) ** 2))
    
    conjecture_holds = correlation > 0.7
    counterexample = "" if conjecture_holds else f"Correlation: {correlation}"
    
    return {
        "metric_name": "Monodromy Group Order vs Resolution Width",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")