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
    
    def generate_d_regular_circuit(d, n):
        if d * n % 2 != 0:
            return None
        circuit = []
        for _ in range(n):
            row = [random.choice([0, 1]) for _ in range(n)]
            circuit.append(row)
        return circuit
    
    def tropicalize(circuit):
        # Simplified tropicalization (not actual Hodge decomposition)
        n = len(circuit)
        tropical_variety = []
        for i in range(n):
            max_val = -math.inf
            for j in range(n):
                if circuit[i][j] > max_val:
                    max_val = circuit[i][j]
            tropical_variety.append(max_val)
        return tropical_variety
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(n):
            for j in range(n):
                if circuit[i][j] == 1:
                    width += 1
        return width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        return numerator / denominator
    
    def wilcoxon_rank_sum_test(x, y):
        n1 = len(x)
        n2 = len(y)
        combined = sorted(x + y)
        ranks = {val: rank for rank, val in enumerate(combined, start=1)}
        sum_ranks_x = sum(ranks[val] for val in x)
        z_stat = (sum_ranks_x - 0.5 * n1 * (n1 + 1)) / math.sqrt(0.25 * n1 * (n1 + 1) * (2 * n1 + 1))
        return z_stat
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        n = len(A)
        rref = gaussian_elimination(A)
        rank = 0
        for row in rref:
            if any(row[i] != 0 for i in range(n)):
                rank += 1
        return rank
    
    n_max = 40
    instances_tested = 30
    thd_values = []
    wm_values = []
    
    for _ in range(instances_tested):
        d = random.randint(2, 5)
        n = random.randint(5, n_max)
        circuit = generate_d_regular_circuit(d, n)
        if circuit is None:
            continue
        thd_value = rank(tropicalize(circuit))
        wm_value = monotone_width(circuit)
        thd_values.append(thd_value)
        wm_values.append(wm_value)
    
    correlation_coefficient = pearson_correlation(thd_values, wm_values)
    z_stat = wilcoxon_rank_sum_test(thd_values, wm_values)
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "Pearson correlation coefficient < 0.7"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
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
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.7\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support_fraction")