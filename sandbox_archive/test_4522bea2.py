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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n+1)]
            clause = ' OR '.join(literals)
            clauses.append(clause)
        return ' AND '.join(clauses)

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(A[i][j]) > abs(A[i_max][j]):
                    i_max = i
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank:
                    factor = A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] -= factor * A[rank][k]
            rank += 1
        return rank

    def minimal_rank_of_quadratic_form(sat_instance):
        # Convert SAT instance to a matrix representation
        n = len(sat_instance.split(' AND '))
        A = [[0] * n for _ in range(n)]
        for clause in sat_instance.split(' AND '):
            literals = clause.split(' OR ')
            for literal in literals:
                if literal.startswith('-'):
                    i = int(literal[2:]) - 1
                    A[i][i] += 1
                else:
                    i = int(literal[1:]) - 1
                    A[i][i] += 1
        return gaussian_elimination(A)

    def resolution_refutation_size(sat_instance):
        # Simplified estimation of resolution refutation size
        n = len(sat_instance.split(' AND '))
        return 2 ** n

    instances_tested = 0
    ranks = []
    refutations = []

    for _ in range(30):  # Ensure at least 30 instances per seed
        sat_instance = generate_sat_instance(random.randint(5, 40))
        rank = minimal_rank_of_quadratic_form(sat_instance)
        refutation_size = resolution_refutation_size(sat_instance)

        ranks.append(rank)
        refutations.append(refutation_size)
        instances_tested += 1

    correlation_coefficient = sum((ranks[i] - mean(ranks)) * (refutations[i] - mean(refutations)) for i in range(instances_tested)) / instances_tested
    mean_rank = mean(ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / instances_tested)

    return {
        "metric_name": "CorrelationCoefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": abs(correlation_coefficient) <= 0.7 and all(abs(corr) <= 0.3 for corr in refutations),
        "counterexample": "" if abs(correlation_coefficient) <= 0.7 else f"Correlation coefficient: {correlation_coefficient}"
    }

def mean(data):
    return sum(data) / len(data)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = mean([r["metric_value"] for r in results])
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in [r["metric_value"] for r in results]) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")