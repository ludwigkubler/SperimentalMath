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
    
    def log2(x):
        if x <= 0:
            return -math.inf
        return math.log2(x)

    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))

    def tseitin_clauses(n):
        clauses = []
        for i in range(n):
            clauses.append([f'x{i}', f'y{i}'])
            clauses.append([f'x{i}', f'z{i}'])
            clauses.append([f'y{i}', f'z{i}'])
        return clauses

    def branching_program(clauses, n):
        program = []
        for i in range(n):
            program.extend([[clauses[i][0], '1'], [clauses[i][1], '2']])
        return program

    def categorical_functor(program):
        functor = {}
        for step in program:
            if step[1] not in functor:
                functor[step[1]] = set()
            functor[step[1]].add(step[0])
        return functor

    def min_rank(functor):
        matrix = []
        for key, values in functor.items():
            row = [0] * len(values)
            for value in values:
                row[list(functor.keys()).index(value)] = 1
            matrix.append(row)
        return rank(matrix)

    n = random.randint(5, 40)
    clauses = tseitin_clauses(n)
    program = branching_program(clauses, n)
    functor = categorical_functor(program)
    min_rank_value = min_rank(functor)

    if min_rank_value <= log2(n):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"IP_2 rank {min_rank_value} > n log n for n={n}"

    return {
        "metric_name": "min_rank",
        "metric_value": min_rank_value,
        "instances_tested": 1,
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

    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")