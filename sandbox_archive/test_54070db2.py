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
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(i, n):
                A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = Fraction(A[k][i])
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A

    def determinant(A):
        n = len(A)
        det = 1
        for i in range(n):
            if A[i][i] == 0:
                return 0
            det *= A[i][i]
        return det

    def matroid_rank(matroid):
        n = len(matroid)
        max_rank = 0
        for i in range(1 << n):
            subset = [j for j in range(n) if (i & (1 << j))]
            submat = [[matroid[j][k] for k in subset] for j in subset]
            rank = sum(1 for row in gaussian_elimination(submat) if any(row))
            max_rank = max(max_rank, rank)
        return max_rank

    def tropical_order(matroid):
        n = len(matroid)
        max_tropical_order = 0
        for i in range(1 << n):
            subset = [j for j in range(n) if (i & (1 << j))]
            submat = [[matroid[j][k] for k in subset] for j in subset]
            rank = sum(1 for row in gaussian_elimination(submat) if any(row))
            max_tropical_order = max(max_tropical_order, rank)
        return max_tropical_order

    def clause_complexity(formula):
        return len(formula)

    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    for n in n_values:
        instances_tested = 0
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = [[random.randint(1, n) for _ in range(random.randint(2, 4))] for _ in range(n)]
            matroid = [[random.choice([0, 1]) if i == j else 0 for j in range(n)] for i in range(n)]
            mto_phi = tropical_order(matroid)
            c_phi = clause_complexity(formula)
            metric_values.append(mto_phi - c_phi)
            instances_tested += 1
        n_max = max(n_values)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    correlation_coefficient = sum(x * y for x, y in zip(metric_values, range(len(metric_values)))) / (len(metric_values) * std_value * (len(metric_values) - 1) ** 0.5)
    
    if correlation_coefficient < 0.8 or abs(std_value) > 3:
        conjecture_holds = False
        counterexample = "correlation_coefficient=<{}> std_value=<{}>".format(correlation_coefficient, std_value)
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "mto(φ) - c(φ)",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_value, std_value, support_fraction))
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(next(r["counterexample"] for r in results if r["counterexample"]), first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")