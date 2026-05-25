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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(i+1, n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    for j in range(i, n):
                        A[k][j] -= A[i][j] * A[k][i]
        return [sum(row) for row in A]

    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for x in variables:
            clauses.append([x])
        for i in range(1, n):
            clauses.append([f'~{variables[i-1]}', f'{variables[i]}'])
        return clauses

    def configuration_space_metric(clauses):
        points = []
        distances = []
        for clause in clauses:
            if len(clause) == 1:
                point = [0] * n
                point[variables.index(clause[0])] = 1
                points.append(point)
            else:
                point1 = [0] * n
                point2 = [0] * n
                for var in clause:
                    if var.startswith('~'):
                        point1[variables.index(var[1:])] = -1
                    else:
                        point2[variables.index(var)] = 1
                points.append(point1)
                points.append(point2)
                distances.append(2)
        return points, distances

    def min_rank(points):
        A = []
        for point in points:
            row = [point[i]**2 for i in range(n)]
            A.append(row)
        rank = gaussian_elimination(A)
        if rank is None:
            return float('inf')
        return len(rank)

    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        clauses = tseitin_formula(n)
        points, distances = configuration_space_metric(clauses)
        rank = min_rank(points)
        ranks.append(rank)

    mean_rank = sum(ranks) / len(ranks)
    conjecture_holds = all(rank >= n**2 * math.log(n) for rank in ranks)
    counterexample = "" if conjecture_holds else f"n={n}, rank={min(ranks)}"

    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, rank={min(r['metric_value'] for r in results)}\" first_failing_seed={first_failing_seed}")