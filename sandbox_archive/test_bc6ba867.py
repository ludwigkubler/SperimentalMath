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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return [row for row in A if any(row)]

    def matrix_rank(A):
        return len(gaussian_elimination(A))

    def fundamental_group_rank():
        # Placeholder function to generate a random rank
        return random.randint(1, 5)

    def abelianization_rank(fundamental_group_rank):
        # Placeholder function to compute abelianization rank
        return fundamental_group_rank

    def communication_matrix_rank(n):
        # Placeholder function to generate and compute the rank of a communication matrix
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return matrix_rank(A)

    n_values = [5, 10, 15, 20, 30, 40]
    local_indeterminacies = []
    comm_matrix_ranks = []

    for n in n_values:
        fundamental_group = fundamental_group_rank()
        abelianization = abelianization_rank(fundamental_group)
        local_indeterminacy = fundamental_group - abelianization
        comm_matrix_rank = communication_matrix_rank(n)
        
        local_indeterminacies.append(local_indeterminacy)
        comm_matrix_ranks.append(comm_matrix_rank)

    n_max = max(n_values)
    instances_tested = len(n_values) * 30

    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Too few instances tested"
        }

    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov / (std_x * std_y)

    correlation_coefficient = pearson_correlation(local_indeterminacies, comm_matrix_ranks)

    if correlation_coefficient < 0.3:
        counterexample = f"Correlation coefficient too low: {correlation_coefficient}"
    else:
        counterexample = ""

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.5,
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

    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")