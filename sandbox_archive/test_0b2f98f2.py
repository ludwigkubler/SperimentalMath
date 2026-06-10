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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def frobenius_norm(A):
        norm = 0
        for row in A:
            for val in row:
                norm += abs(val) ** 2
        return math.sqrt(norm)

    def geometric_invariant_rank(A):
        U, _, Vt = gaussian_elimination(matrix_multiplication(A, A))
        rank = sum(1 for row in U if any(row))
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    gir_values = []
    
    for n in n_values:
        phi_G = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        gir_value = geometric_invariant_rank(phi_G)
        gir_values.append(gir_value)

    if not gir_values:
        return {
            "metric_name": "geometric_invariant_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_gir = sum(gir_values) / len(gir_values)
    std_gir = math.sqrt(sum((x - mean_gir) ** 2 for x in gir_values) / len(gir_values))
    correlation_coefficient = (len(gir_values) * sum(x * y for x, y in zip(n_values, gir_values)) -
                                sum(n_values) * sum(gir_values)) / \
                               math.sqrt((len(gir_values) * sum(x ** 2 for x in n_values) - sum(n_values) ** 2) *
                                         (len(gir_values) * sum(y ** 2 for y in gir_values) - sum(gir_values) ** 2))

    return {
        "metric_name": "geometric_invariant_rank",
        "metric_value": mean_gir,
        "instances_tested": len(gir_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient:.2f} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 9973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gir = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_gir = math.sqrt(sum((r["metric_value"] - mean_gir) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_gir:.2f} std={std_gir:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")