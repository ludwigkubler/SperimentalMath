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
    
    def generate_geometric_circuit(n):
        if n == 5:
            return [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]]
        elif n == 10:
            return [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 0]]
        elif n == 15:
            return [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 0]]
        elif n == 20:
            return [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [15, 16], [16, 17], [17, 18], [18, 19], [19, 0]]
        elif n == 30:
            return [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [15, 16], [16, 17], [17, 18], [18, 19], [19, 20], [20, 21], [21, 22], [22, 23], [23, 24], [24, 25], [25, 26], [26, 27], [27, 28], [28, 29], [29, 0]]
        elif n == 40:
            return [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [15, 16], [16, 17], [17, 18], [18, 19], [19, 20], [20, 21], [21, 22], [22, 23], [23, 24], [24, 25], [25, 26], [26, 27], [27, 28], [28, 29], [29, 30], [30, 31], [31, 32], [32, 33], [33, 34], [34, 35], [35, 36], [36, 37], [37, 38], [38, 39], [39, 0]]
        else:
            raise ValueError("Unsupported n value")

    def incidence_algebra(G):
        n = len(G)
        A_G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    A_G[i][j] = sum(len(set(G[k]) & set(G[l])) for k in range(n) if k != i and k != j)
        return A_G

    def communication_complexity_rank(A_G):
        n = len(A_G)
        rank = 0
        for i in range(n):
            row_sum = sum(A_G[i])
            if row_sum > 0:
                rank += 1
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        G = generate_geometric_circuit(n)
        A_G = incidence_algebra(G)
        r_G = communication_complexity_rank(A_G)
        i_G = sum(sum(row) for row in A_G) / (n * (n - 1))
        results.append({"n": n, "i_G": i_G, "r_G": r_G})

    metric_name = "correlation"
    metric_value = sum(result["i_G"] * result["r_G"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = False
    counterexample = ""

    if instances_tested >= 30:
        # Calculate Pearson correlation coefficient
        mean_i_G = sum(result["i_G"] for result in results) / instances_tested
        mean_r_G = sum(result["r_G"] for result in results) / instances_tested
        numerator = sum((result["i_G"] - mean_i_G) * (result["r_G"] - mean_r_G) for result in results)
        denominator = math.sqrt(sum((result["i_G"] - mean_i_G) ** 2 for result in results)) * math.sqrt(sum((result["r_G"] - mean_r_G) ** 2 for result in results))
        correlation_coefficient = numerator / denominator if denominator != 0 else 0

        # Check significance level
        t_statistic = correlation_coefficient * math.sqrt(instances_tested - 2) / math.sqrt(1 - correlation_coefficient ** 2)
        p_value = 2 * (1 - stats.t.cdf(abs(t_statistic), instances_tested - 2))

        if correlation_coefficient >= 0.7 and p_value <= 0.05:
            conjecture_holds = True

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "first failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")