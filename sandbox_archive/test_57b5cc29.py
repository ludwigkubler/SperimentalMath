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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_boolean_circuit(n // 2) for _ in range(2)]
            return [subcircuits[0][i] ^ subcircuits[1][i] for i in range(len(subcircuits[0]))]
    
    def communication_complexity_rank(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        else:
            left_rank = communication_complexity_rank(circuit[:n // 2])
            right_rank = communication_complexity_rank(circuit[n // 2:])
            return max(left_rank, right_rank) + 1
    
    def von_neumann_algebra(circuit):
        n = len(circuit)
        algebra = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if circuit[i] == circuit[j]:
                    algebra[i][j] = 1
                    algebra[j][i] = 1
        return algebra
    
    def minimal_local_indefinite_integral(algebra):
        n = len(algebra)
        trace = sum(algebra[i][i] for i in range(n))
        determinant = 1
        for i in range(n):
            for j in range(i + 1, n):
                if algebra[i][j] != 0:
                    for k in range(j, n):
                        algebra[k][j] -= algebra[k][i] * algebra[j][k]
                    trace += algebra[j][i] * algebra[i][j]
                    determinant *= algebra[i][j]
        return trace / determinant
    
    def correlation(a, b):
        mean_a = sum(a) / len(a)
        mean_b = sum(b) / len(b)
        cov = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(len(a))) / len(a)
        std_a = math.sqrt(sum((x - mean_a) ** 2 for x in a) / len(a))
        std_b = math.sqrt(sum((y - mean_b) ** 2 for y in b) / len(b))
        return cov / (std_a * std_b)
    
    def mean_absolute_difference(a, b):
        return sum(abs(x - y) for x, y in zip(a, b)) / len(a)
    
    n_values = [5, 10, 15, 20, 30, 40]
    lii_values = []
    rank_comm_values = []
    
    for n in n_values:
        circuits = [generate_boolean_circuit(n) for _ in range(30)]
        for circuit in circuits:
            algebra = von_neumann_algebra(circuit)
            lii = minimal_local_indefinite_integral(algebra)
            rank_comm = communication_complexity_rank(circuit)
            lii_values.append(lii)
            rank_comm_values.append(rank_comm)
    
    correlation_value = correlation(lii_values, rank_comm_values)
    mean_diff = mean_absolute_difference(lii_values, rank_comm_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_value,
        "instances_tested": len(lii_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_value >= 0.8 and mean_diff <= 3,
        "counterexample": "" if correlation_value >= 0.8 and mean_diff <= 3 else "correlation < 0.8 or mean_abs_diff > 3"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")