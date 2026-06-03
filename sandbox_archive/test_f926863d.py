# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_rank(A):
        A_rref = gaussian_elimination([row[:] for row in A])
        rank = 0
        for row in A_rref:
            if any(row):
                rank += 1
        return rank

    def fundamental_group_rank(n):
        # Simulate the rank of the fundamental group (example: n generators)
        return n

    def abelianization_rank(n):
        # Simulate the rank of the abelianization (example: n-1 generators)
        return n - 1

    def communication_matrix_rank(n):
        # Simulate a random communication matrix and compute its rank
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return matrix_rank(A)

    n_values = [5, 10, 15, 20, 30, 40]
    local_indeterminacies = []
    comm_matrix_ranks = []

    for n in n_values:
        f_group_rank = fundamental_group_rank(n)
        abelian_rank = abelianization_rank(n)
        local_indeterminacy = f_group_rank - abelian_rank
        comm_matrix_rank_val = communication_matrix_rank(n)

        local_indeterminacies.append(local_indeterminacy)
        comm_matrix_ranks.append(comm_matrix_rank_val)

    if not local_indeterminacies or not comm_matrix_ranks:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }

    n = len(local_indeterminacies)
    mean_local_indeterminacy = sum(local_indeterminacies) / n
    mean_comm_matrix_rank = sum(comm_matrix_ranks) / n

    covariance = sum((local_indeterminacies[i] - mean_local_indeterminacy) * (comm_matrix_ranks[i] - mean_comm_matrix_rank) for i in range(n)) / n
    variance_local_indeterminacy = sum((local_indeterminacies[i] - mean_local_indeterminacy) ** 2 for i in range(n)) / n
    variance_comm_matrix_rank = sum((comm_matrix_ranks[i] - mean_comm_matrix_rank) ** 2 for i in range(n)) / n

    pearson_corr_coeff = covariance / (variance_local_indeterminacy * variance_comm_matrix_rank) ** 0.5

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr_coeff >= 0.5 and all(pearson_corr_coeff >= 0.3 for _ in range(n)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and all(result["metric_value"] >= 0.3 for result in results):
        print("RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")