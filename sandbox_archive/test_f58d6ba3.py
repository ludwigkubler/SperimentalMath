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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = 0
        if m == 1:
            return A[0][0]
        elif m == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for j in range(n):
                det += ((-1) ** j) * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
        return det
    
    def is_polynomial_time_computable(protocol_complexity):
        # Placeholder function to simulate polynomial-time computability
        return True
    
    def count_non_zero_cells(deligne_lusztig_cells):
        # Placeholder function to count non-zero cells
        return sum(cell != 0 for cell in deligne_lusztig_cells)
    
    n = random.randint(5, 40)
    protocol_complexity = n * (n - 1) // 2
    
    if not is_polynomial_time_computable(protocol_complexity):
        return {
            "metric_name": "non_zero_cells",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    deligne_lusztig_cells = [random.randint(0, 1) for _ in range(protocol_complexity)]
    non_zero_count = count_non_zero_cells(deligne_lusztig_cells)
    
    return {
        "metric_name": "non_zero_cells",
        "metric_value": non_zero_count,
        "instances_tested": 1,
        "conjecture_holds": non_zero_count >= protocol_complexity ** 3,
        "counterexample": "" if non_zero_count >= protocol_complexity ** 3 else f"Protocol complexity {protocol_complexity}, non-zero cells {non_zero_count}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")