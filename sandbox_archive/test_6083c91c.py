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
    
    def matrix_det(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * matrix_det(submatrix)
        return det
    
    def free_entropy(P):
        n = len(P)
        eigenvalues = []
        for i in range(n):
            for j in range(n):
                if i != j:
                    submatrix = [[P[k][l] if (k != i and l != j) else 1 - P[k][l] for l in range(n)] for k in range(n)]
                    eigenvalues.append(matrix_det(submatrix))
        return sum(math.log(abs(e)) for e in eigenvalues) / n
    
    def generate_bp(n):
        bp = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.choice([True, False]):
                    bp[i][j] = 1
                    bp[j][i] = 1
        return bp
    
    def is_read_twice(bp):
        n = len(bp)
        for i in range(n):
            for j in range(i+1, n):
                if bp[i][j] == 0:
                    continue
                for k in range(j+1, n):
                    if bp[j][k] == 0 and bp[k][i] == 0:
                        return True
        return False
    
    n = 40
    P = generate_bp(n)
    
    if not is_read_twice(P):
        return {
            "metric_name": "free_entropy",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    chi_P = free_entropy(P)
    
    if chi_P is None:
        return {
            "metric_name": "free_entropy",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "free_entropy",
        "metric_value": chi_P,
        "instances_tested": 1,
        "conjecture_holds": True if chi_P >= math.sqrt(n) * math.log(n) else False,
        "counterexample": "" if chi_P >= math.sqrt(n) * math.log(n) else f"chi(P) = {chi_P}, expected Ω(√{n} log {n})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    total_metric_value = 0
    count_supporting = 0
    counterexamples = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["conjecture_holds"]:
            total_metric_value += trial_result["metric_value"]
            count_supporting += 1
        else:
            counterexamples.append(trial_result["counterexample"])
    
    mean_metric_value = total_metric_value / len(seeds)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in [r["metric_value"] for r in run_trial(seed) for seed in seeds]) / len(seeds))
    support_fraction = count_supporting / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif counterexamples:
        first_counterexample = counterexamples[0]
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample}\" first_failing_seed={seeds[counterexamples.index(first_counterexample)]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")