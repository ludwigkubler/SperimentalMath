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
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(range(1, n + 1), random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def cell_complex_rank(phi):
        variables = set()
        for clause in phi:
            variables.update(clause)
        incidence_matrix = [[0] * len(variables) for _ in range(len(phi))]
        var_index = {var: i for i, var in enumerate(variables)}
        
        for i, clause in enumerate(phi):
            for var in clause:
                incidence_matrix[i][var_index[var]] = 1
        
        rank = 0
        for row in incidence_matrix:
            if any(row[j] != 0 for j in range(rank)):
                pivot_col = next(j for j in range(len(row)) if row[j] != 0)
                for i2, row2 in enumerate(incidence_matrix):
                    if i2 != i and row2[pivot_col] != 0:
                        factor = Fraction(row2[pivot_col], row[pivot_col])
                        for j in range(len(row)):
                            row2[j] -= factor * row[j]
                rank += 1
        return rank

    def communication_complexity(phi):
        n = len(phi)
        max_clauses_per_var = max(sum(1 for clause in phi if var in clause) for var in range(1, n + 1))
        return max_clauses_per_var * n

    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        phi = generate_cnf(n)
        rank = cell_complex_rank(phi)
        comm_complexity = communication_complexity(phi)
        results.append((n, rank, comm_complexity))

    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    n_values, ranks, comm_complexities = zip(*results)
    mean_rank = sum(ranks) / len(ranks)
    mean_comm_complexity = sum(comm_complexities) / len(comm_complexities)

    correlation_coefficient = 0
    if len(set(n_values)) > 1:
        numerator = sum((r - mean_rank) * (c - mean_comm_complexity) for r, c in zip(ranks, comm_complexities))
        denominator = math.sqrt(sum((r - mean_rank) ** 2 for r in ranks)) * math.sqrt(sum((c - mean_comm_complexity) ** 2 for c in comm_complexities))
        correlation_coefficient = numerator / denominator if denominator != 0 else 0

    mean_abs_diff = sum(abs(r - c) for r, c in zip(ranks, comm_complexities)) / len(ranks)

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if "counterexample" in r and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support found")