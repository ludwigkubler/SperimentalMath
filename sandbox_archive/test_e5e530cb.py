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
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            cnf.append(clause)
        return cnf
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            max_row = rank
            for j in range(rank, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            if matrix[max_row][i] == 0:
                continue
            matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
            for j in range(cols):
                if j != i and matrix[rank][j] != 0:
                    factor = -matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[rank][k]
            rank += 1
        return rank
    
    def minimal_order(cnf):
        n = len(cnf)
        identity_matrix = [[int(i == j) for j in range(n)] for i in range(n)]
        augmented_matrix = [row + [1] for row in cnf] + identity_matrix
        rank = gaussian_elimination(augmented_matrix)
        return rank
    
    def monotone_width(cnf):
        n = len(cnf)
        max_clauses = 0
        for i in range(1 << n):
            clauses = sum(1 for clause in cnf if any(lit in bin(i)[2:] for lit in clause))
            if clauses > max_clauses:
                max_clauses = clauses
        return max_clauses
    
    instances_tested = 0
    total_order = 0
    total_width = 0
    n_max = 0
    
    for m in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(40, m)
            instances_tested += 1
            order = minimal_order(cnf)
            width = monotone_width(cnf)
            total_order += order
            total_width += width
            if n_max < m:
                n_max = m
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(order * width for order, width in zip([mean_order] * instances_tested, [mean_width] * instances_tested)) - instances_tested * mean_order * mean_width) / math.sqrt((instances_tested * sum(order ** 2 for order in [mean_order] * instances_tested) - instances_tested * mean_order ** 2) * (instances_tested * sum(width ** 2 for width in [mean_width] * instances_tested) - instances_tested * mean_width ** 2))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient<0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.9:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.7\" first_failing_seed={next(seed for seed, res in enumerate(results) if not res['conjecture_holds'])}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction<{support_fraction} < 0.9")