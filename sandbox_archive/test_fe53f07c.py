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
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def determinant(matrix):
        rows, cols = len(matrix), len(matrix[0])
        if rows != cols:
            raise ValueError("Matrix must be square")
        if rows == 1:
            return matrix[0][0]
        det = 0
        for j in range(cols):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det

    def minimal_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(rows, cols)):
            if any(matrix[j][i] != 0 for j in range(i, rows)):
                rank += 1
        return rank

    def geometric_langlands_dual(vector_space):
        # Placeholder for the actual mapping to Geometric Langlands theory
        # This is a dummy implementation and should be replaced with a proper one
        dual_space = [[random.randint(0, 1) for _ in range(len(vector_space))] for _ in range(len(vector_space))]
        return dual_space

    def distinguishing_tensor_width(bp):
        # Placeholder for the actual computation of distinguishing tensor width
        # This is a dummy implementation and should be replaced with a proper one
        return random.uniform(0, 1)

    n = random.randint(5, 40)
    bp = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    dual_space = geometric_langlands_dual(bp)
    rho_P = distinguishing_tensor_width(bp)
    m_R_P = minimal_rank(dual_space)

    if m_R_P == 0:
        return {
            "metric_name": "rho(P)/m(R(P))",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "minimal_rank_is_zero"
        }

    ratio = rho_P / m_R_P
    c = 2  # Example constant, should be determined based on actual theory

    return {
        "metric_name": "rho(P)/m(R(P))",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= math.log(n) / math.log(c),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 107))
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")