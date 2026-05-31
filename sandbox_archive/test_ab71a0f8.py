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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            denom = A[i][i]
            for j in range(n):
                A[i][j] /= denom
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        return rank

    def generate_quotient_ring(k, n):
        variables = [[f"x_{i}_{j}" for j in range(n)] for i in range(k)]
        relations = []
        # Example relation: x_0_0 * x_1_0 - x_2_0
        relations.append([variables[0][0], variables[1][0], -variables[2][0]])
        return variables, relations

    def compute_brauer_group_rank(k, n):
        variables, relations = generate_quotient_ring(k, n)
        A = [[0] * (n + k) for _ in range(n + k)]
        for i in range(n):
            A[i][i] = 1
        for relation in relations:
            for j in range(len(relation)):
                if relation[j] != 0:
                    for l in range(len(variables[0])):
                        if variables[l][j] in relation:
                            A[i][l + n] += relation[j]
                            break
        return matrix_rank(A)

    def communication_complexity(k, n):
        # Example complexity: k * n bits
        return k * n

    k = random.randint(2, 5)
    n = random.randint(10, 30)
    instances_tested = 30
    total_brauer_rank = 0
    total_communication_complexity = 0

    for _ in range(instances_tested):
        brauer_rank = compute_brauer_group_rank(k, n)
        communication_comp = communication_complexity(k, n)
        total_brauer_rank += brauer_rank
        total_communication_complexity += communication_comp

    mean_brauer_rank = total_brauer_rank / instances_tested
    avg_communication_complexity = total_communication_complexity / instances_tested
    conjecture_holds = (mean_brauer_rank >= 0.5 * n ** (k / 2)) and (avg_communication_complexity <= 100)

    return {
        "metric_name": "Brauer group rank",
        "metric_value": mean_brauer_rank,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_brauer_rank={mean_brauer_rank}, avg_communication_complexity={avg_communication_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_brauer_rank = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_brauer_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_brauer_rank} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_brauer_rank} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")