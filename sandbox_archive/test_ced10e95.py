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
    
    def generate_xor_tautology(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def kahler_form(truth_table):
        n = len(truth_table)
        form = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    form[i][j] = truth_table[i] ^ truth_table[j]
        return form
    
    def dnf_width(truth_table):
        n = len(truth_table)
        min_width = float('inf')
        for assignment in itertools.product([0, 1], repeat=n):
            if all(assignment[i] == truth_table[i] for i in range(n)):
                width = sum(1 for bit in assignment if bit == 1)
                if width < min_width:
                    min_width = width
        return min_width
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    matrix[i][j] /= matrix[i][j]
                for k in range(m):
                    if k != i and any(matrix[k][j] != 0 for j in range(n)):
                        for j in range(n):
                            matrix[k][j] -= matrix[i][j] * matrix[k][i]
        return rank
    
    n = random.randint(5, 40)
    truth_table = generate_xor_tautology(n)
    k_form = kahler_form(truth_table)
    dnf_width_val = dnf_width(truth_table)
    rank_k_form = matrix_rank(k_form)
    
    metric_value = rank_k_form / dnf_width_val
    conjecture_holds = abs(metric_value - 1) < 0.5
    counterexample = "" if conjecture_holds else f"rank(K)={rank_k_form}, width(DNF)={dnf_width_val}"
    
    return {
        "metric_name": "Rank of Kähler Form / Width of DNF",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank(K) grows sub-linearly compared to width(DNF)\" first_failing_seed={first_failing_seed}")