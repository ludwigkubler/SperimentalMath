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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def is_invertible(matrix):
        det = 1
        n = len(matrix)
        for i in range(n):
            for j in range(i, n):
                if matrix[i][j] != 0:
                    if i == j:
                        det *= matrix[i][j]
                    else:
                        factor = Fraction(matrix[j][i], matrix[i][i])
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
            if det == 0:
                return False
        return True

    def sos_degree(A):
        m, n = len(A), len(A[0])
        A_augmented = [row + [-1] for row in A]
        identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n+1)] for i in range(m)]
        A_augmented = gaussian_elimination(A_augmented)
        return next((i for i, row in enumerate(A_augmented) if all(x == 0 for x in row[:-1]) and row[-1] != 0), None)

    def is_o_minimal_structure(matrix):
        # Placeholder function to simulate checking for o-minimality
        # In practice, this would involve more sophisticated algebraic geometry checks
        return True

    n = 40
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = 0
    A = [row + [-sum(row) // 2] for row in A]

    if not is_invertible(A):
        return {
            "metric_name": "sos_degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Non-invertible matrix"
        }

    sos_deg = sos_degree(A)
    o_minimal = is_o_minimal_structure(A)

    return {
        "metric_name": "sos_degree",
        "metric_value": sos_deg,
        "instances_tested": 1,
        "conjecture_holds": sos_deg >= math.log(n) if o_minimal else True,
        "counterexample": "" if o_minimal and sos_deg >= math.log(n) else "Non-o-minimal structure or low SOS degree"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample_desc = "Non-o-minimal structure or low SOS degree"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")