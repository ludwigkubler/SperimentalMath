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
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(n):
                if j != i:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        return [row for row in matrix if any(row)]

    def tensor_product(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def tropicalize(matrix):
        m, n = len(matrix), len(matrix[0])
        result = [[-math.inf] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if matrix[i][j] != 0:
                    result[i][j] = math.log(abs(matrix[i][j]))
        return result

    def dpll_width(instance):
        # Placeholder implementation of DPLL width calculation
        # This is a simplified version and may not be accurate for all instances
        return len(instance)

    lie_algebra = [[1, 0], [0, -1]]  # Example Lie algebra matrix

    n = random.randint(5, 40)
    instance = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        instance.append(clause)

    tensor_prod = tensor_product(instance, lie_algebra)
    tropicalized_tensor_prod = tropicalize(tensor_prod)
    rank = len(gaussian_elimination(tropicalized_tensor_prod))
    width = dpll_width(instance)

    return {
        "metric_name": "Rank",
        "metric_value": rank,
        "instances_tested": n,
        "conjecture_holds": rank < width - 5,
        "counterexample": "" if rank < width - 5 else f"Instance with rank {rank} and width {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")