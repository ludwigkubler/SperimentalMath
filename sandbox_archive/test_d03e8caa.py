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
        n = len(matrix)
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(matrix[k][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            matrix[i] = [x * factor for x in matrix[i]]
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    matrix[j] = [matrix[j][k] - factor * matrix[i][k] for k in range(n)]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(matrix[k][i]))
            if max_row != i:
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                det *= -1
            factor = matrix[i][i]
            if factor == 0:
                return 0
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(i + 1, n):
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        det *= [matrix[i][i] for i in range(n)]
        return det

    def secant_variety(X):
        n = len(X)
        V_X = []
        for x1, x2 in itertools.combinations(X, 2):
            row = [x1[i] + x2[i] for i in range(n)]
            V_X.append(row)
        return V_X

    def noncommutative_Lp_entropy(V_X):
        n = len(V_X[0])
        p = 2  # Example value for p
        entropy = 0
        for v in V_X:
            norm = sum(abs(x) ** p for x in v) ** (1 / p)
            entropy += math.log(norm)
        return entropy

    n = random.randint(5, 40)
    X = [random.random() for _ in range(n)]
    V_X = secant_variety(X)
    H_mu_VX = noncommutative_Lp_entropy(V_X)
    
    metric_name = "noncommutative_Lp_entropy"
    metric_value = H_mu_VX
    instances_tested = 1
    conjecture_holds = H_mu_VX >= n
    counterexample = "" if conjecture_holds else f"n={n}, H_mu(V_X)={H_mu_VX}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")