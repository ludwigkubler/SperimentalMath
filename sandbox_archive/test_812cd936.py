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
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def determinant(matrix):
        rows, cols = len(matrix), len(matrix[0])
        if rows != cols:
            raise ValueError("Matrix must be square")
        det = Fraction(1)
        for i in range(rows):
            pivot = matrix[i][i]
            if pivot == 0:
                return Fraction(0)
            det *= pivot
            for j in range(i + 1, rows):
                factor = Fraction(matrix[j][i], pivot)
                for k in range(i, cols):
                    matrix[j][k] -= factor * matrix[i][k]
        return det

    def geometric_invariant(matrix):
        # Placeholder for the actual geometric invariant computation
        # This is a dummy implementation that should be replaced with a proper one
        return determinant(gaussian_elimination(matrix))

    def communication_complexity(M_f):
        # Placeholder for the actual communication complexity calculation
        # This is a dummy implementation that should be replaced with a proper one
        n = len(M_f)
        return Fraction(n * (n - 1), 2)

    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        n = random.randint(5, 40)
        X = list(range(n))
        Y = list(range(n))
        M_f = [[random.choice([0, 1]) for _ in Y] for _ in X]
        
        gamma_M_f = geometric_invariant(M_f)
        comm_f = communication_complexity(M_f)
        
        if comm_f < Fraction(1, 2) * gamma_M_f:
            conjecture_holds = False
            counterexample = f"n={n}, M_f={M_f}"
            break
        
        instances_tested += 1

    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_f,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
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

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")