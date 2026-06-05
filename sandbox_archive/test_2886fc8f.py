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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_boolean_circuit(n // 2)
            right = generate_boolean_circuit(n - n // 2)
            return [(x and y) for x in left] + [(x or y) for y in right]
    
    def monotone_width(circuit):
        if len(circuit) == 1:
            return 1
        else:
            return max(monotone_width(circuit[:len(circuit)//2]), monotone_width(circuit[len(circuit)//2:]))
    
    def tropical_module(circuit):
        n = len(circuit)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            M[i][i-1] = circuit[i-1]
        for j in range(2, n + 1):
            for i in range(j - 1, 0, -1):
                M[i][j-1] = max(M[i][j-2], M[i+1][j-2])
        return M
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j] != 0:
                    pivot_row = i
                    break
            else:
                continue
            for k in range(j, n):
                matrix[pivot_row][k], matrix[i][k] = matrix[i][k], matrix[pivot_row][k]
            for l in range(m):
                if l != pivot_row and matrix[l][j] != 0:
                    factor = -matrix[l][j] / matrix[pivot_row][j]
                    for k in range(j, n):
                        matrix[l][k] += factor * matrix[pivot_row][k]
        return sum(1 for row in matrix if any(row[i] != 0 for i in range(n)))
    
    total_ranks = []
    total_widths = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_boolean_circuit(n)
            width = monotone_width(circuit)
            if width == 0:
                continue
            M = tropical_module(circuit)
            r_trop = rank(M)
            total_ranks.append(r_trop)
            total_widths.append(width)
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_rank = sum(total_ranks) / len(total_ranks)
    mean_width = sum(total_widths) / len(total_widths)
    correlation_coefficient = (sum((r - mean_rank) * (w - mean_width) for r, w in zip(total_ranks, total_widths)) /
                               math.sqrt(sum((r - mean_rank)**2 for r in total_ranks)) *
                               math.sqrt(sum((w - mean_width)**2 for w in total_widths)))
    
    conjecture_holds = correlation_coefficient > 0.8 and (mean_rank / mean_width) <= 1.5
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or mean_rank / mean_width > 1.5"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")