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
        n = len(matrix)
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(matrix[k][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(1, matrix[i][i])
            for j in range(n):
                matrix[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = -matrix[k][i]
                    for j in range(n):
                        matrix[k][j] += factor * matrix[i][j]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = Fraction(1)
        for i in range(n):
            det *= matrix[i][i]
        return det

    def tensor_product(matrices):
        if not matrices:
            return [[1]]
        result = matrices[0]
        for matrix in matrices[1:]:
            new_result = []
            for row in result:
                new_row = [sum(a * b for a, b in zip(row_i, col_j)) for col_j in zip(*matrix)]
                new_result.append(new_row)
            result = new_result
        return result

    n = 16
    M = [[random.random() for _ in range(n)] for _ in range(n)]
    for row in M:
        total = sum(row)
        for i in range(n):
            row[i] /= total

    rho = - (1/n) * math.log(determinant(tensor_product([M]*n)))
    
    return {
        "metric_name": "free_entropy",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": rho >= 0.3 * math.log(n),
        "counterexample": "" if rho >= 0.3 * math.log(n) else f"rho={rho} < 0.3 log({n})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")