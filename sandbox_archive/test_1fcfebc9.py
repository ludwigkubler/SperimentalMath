# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = None
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for j in range(rows):
                    if j != rank:
                        factor = -matrix[j][i] / matrix[rank][i]
                        for k in range(cols):
                            matrix[j][k] += factor * matrix[rank][k]
                rank += 1
        return rank
    
    def minimal_order(cnf):
        n = len(cnf)
        identity_matrix = [[Fraction(0) if i != j else Fraction(1) for j in range(n)] for i in range(n)]
        augmented_matrix = [row + [lit] for row, lit in zip(cnf, range(1, n+1))]
        rank = gaussian_elimination(augmented_matrix)
        return rank
    
    def monotone_width(cnf):
        n = len(cnf)
        if n == 0:
            return 0
        max_width = 0
        for i in range(2**n):
            clause_set = set()
            for j in range(n):
                if (i >> j) & 1:
                    clause_set.add(j + 1)
                else:
                    clause_set.add(-(j + 1))
            if all(lit in bin(i)[2:] for lit in clause_set):
                max_width = max(max_width, len(clause_set))
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(1, n)
            cnf = generate_cnf(n, m)
            order = minimal_order(cnf)
            total_order += order
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_order = total_order / instances_tested
    
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "Minimal Order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.9:
        print("RESULT: FALSIFIED counterexample='correlation_below_threshold' first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")