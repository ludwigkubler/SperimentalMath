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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def incidence_matrix(instance):
        n = int(math.log2(len(instance)))
        I = [[0] * (2**n) for _ in range(n)]
        for i in range(n):
            for j in range(2**(i+1)):
                if instance[j] == 1:
                    I[i][j] = 1
                    I[i][j ^ (1 << i)] = 1
        return I
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def resolution_width(instance):
        n = int(math.log2(len(instance)))
        clauses = [tuple([i for i, bit in enumerate(instance) if bit == 1])]
        while True:
            new_clauses = []
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1).intersection(clause2)) > 0:
                        diff = list(set(clause1) ^ set(clause2))
                        if len(diff) == 1:
                            new_clauses.append(tuple(sorted(list(set(clause1) - {diff[0]}))))
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return max(len(clause) for clause in clauses)
    
    def conjugacy_classes(matrix):
        n = len(matrix)
        G = []
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] == 1 and matrix[j][i] == 0:
                    G.append((i, j))
        return len(G) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_conjugacy_classes = 0
    total_resolution_width = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            instance = generate_boolean_instance(n)
            I = incidence_matrix(instance)
            cc = conjugacy_classes(I)
            w = resolution_width(instance)
            instances_tested += 1
            total_conjugacy_classes += cc
            total_resolution_width += w
            max_n = max(max_n, n)
    
    mean_cc = total_conjugacy_classes / instances_tested
    mean_w = total_resolution_width / instances_tested
    
    conjecture_holds = mean_cc <= (5 * max_n / 3) and mean_w <= (2 * max_n)
    counterexample = "" if conjecture_holds else f"mean_cc={mean_cc}, mean_w={mean_w}"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_w,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")