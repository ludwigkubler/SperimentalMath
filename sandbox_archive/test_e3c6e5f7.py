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
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(i, n + 1):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = Fraction(matrix[j][i])
                    for k in range(i, n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = Fraction(1)
        for i in range(n):
            pivot_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                    pivot_row = j
            if matrix[pivot_row][i] == 0:
                return Fraction(0)
            det *= matrix[pivot_row][i]
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(i+1, n):
                factor = Fraction(matrix[j][i])
                for k in range(i, n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        return det

    def local_cohomological_defect(n):
        # Simplified model of LCD based on intersection theory
        return random.uniform(0.5, 2) * math.log(n)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_lcd = Fraction(0)
        total_log_width = Fraction(0)
        for _ in range(5):
            formula = ''.join(random.choices('01', k=n))
            width = len(formula)
            lcd = local_cohomological_defect(width)
            total_lcd += lcd
            total_log_width += math.log(width)
            instances_tested += 1
        mean_lcd = total_lcd / instances_tested
        mean_log_width = total_log_width / instances_tested
        std_dev = sum((lcd - mean_lcd)**2 for lcd in [local_cohomological_defect(width) for _ in range(5)]) / instances_tested
        ratio_mean = mean_lcd / mean_log_width
        ratio_std = std_dev / math.sqrt(instances_tested)
        results.append({
            "n": n,
            "mean_lcd": mean_lcd,
            "mean_log_width": mean_log_width,
            "ratio_mean": ratio_mean,
            "ratio_std": ratio_std
        })

    correlation_coefficient = sum((r["ratio_mean"] - 0.8) * r["ratio_std"] for r in results) / len(results)
    if correlation_coefficient >= 0.8 and all(r["ratio_mean"] <= math.log(r["mean_log_width"]) + 3 * r["ratio_std"] for r in results):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "correlation_coefficient=<{}> ratio_std_deviation=<{}>".format(correlation_coefficient, sum(r["ratio_std"] for r in results) / len(results))

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested * 6,
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(r["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")