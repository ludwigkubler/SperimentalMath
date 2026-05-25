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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for j in range(rows):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rref_matrix = gaussian_elimination(matrix)
        rank = 0
        for row in rref_matrix:
            if any(row):
                rank += 1
        return rank

    def generate_quandle(m):
        generators = [random.randint(0, 1) for _ in range(m)]
        quandle = {}
        for i in range(m):
            for j in range(m):
                quandle[(i, j)] = (generators[i] + generators[j]) % 2
        return quandle

    def abelian_subgroup_size(quandle):
        m = len(quandle)
        subgroup = {0}
        for i in range(1, m):
            if all(quandle[(i, j)] == quandle[(0, j)] for j in range(m)):
                subgroup.add(i)
        return 2 ** len(subgroup)

    def k_clique_lower_bound(k, m):
        return math.ceil(2 ** (k / 2) * m)

    n = random.randint(5, 40)
    quandle = generate_quandle(n)
    abelian_size = abelian_subgroup_size(quandle)
    rho_Q = rank([[quandle[(i, j)] for i in range(n)] for j in range(n)])
    
    k = random.randint(3, 10)
    lower_bound = k_clique_lower_bound(k, n)

    return {
        "metric_name": "Minimal Rank of Quandle Representation",
        "metric_value": rho_Q,
        "instances_tested": 1,
        "conjecture_holds": rho_Q > lower_bound if abelian_size == 2 else rho_Q <= lower_bound + abelian_size - 1,
        "counterexample": "" if rho_Q > lower_bound or (rho_Q <= lower_bound + abelian_size - 1 and abelian_size != 2) else f"Quandle with {n} generators, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")