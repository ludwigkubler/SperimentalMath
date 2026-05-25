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
    
    def incidence_structure(C):
        n = len(C)
        I = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if C[i][j]:
                    I[i][j] = 1
                    I[j][i] = 1
        return I
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(A[i][j]) > abs(A[i_max][j]):
                    i_max = i
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank and A[i][j] != 0:
                    factor = -A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] += factor * A[rank][k]
            rank += 1
        return rank
    
    def minimal_order(I):
        n = len(I)
        I_ext = [row + [0] * (n - len(row)) for row in I]
        rank = gaussian_elimination(I_ext)
        return Fraction(n, rank) if rank > 0 else float('inf')
    
    def generate_monotone_k_clique_circuit(k):
        n = random.randint(5, 40)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < k / (n * (n - 1) / 2):
                    C[i][j] = 1
                    C[j][i] = 1
        return C
    
    def is_quasi_crystalline(I):
        # Placeholder for actual quasi-crystalline check
        return True
    
    n_tests = 30
    total_order = 0
    support_count = 0
    
    for _ in range(n_tests):
        k = random.randint(2, 5)
        C = generate_monotone_k_clique_circuit(k)
        I = incidence_structure(C)
        
        if not is_quasi_crystalline(I):
            return {
                "metric_name": "minimal_order",
                "metric_value": float('inf'),
                "instances_tested": n_tests,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        order = minimal_order(I)
        total_order += order
        
        if order <= Fraction(n_tests * k, 2) * math.log(n_tests):
            support_count += 1
    
    mean_order = total_order / n_tests
    std_dev = (sum((order - mean_order) ** 2 for order in range(n_tests)) / n_tests) ** 0.5
    support_fraction = support_count / n_tests
    
    if support_fraction >= 0.8:
        return {
            "metric_name": "minimal_order",
            "metric_value": mean_order,
            "instances_tested": n_tests,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        for _ in range(n_tests):
            k = random.randint(2, 5)
            C = generate_monotone_k_clique_circuit(k)
            I = incidence_structure(C)
            order = minimal_order(I)
            if order > Fraction(n_tests * k, 2) * math.log(n_tests) * 1.5:
                return {
                    "metric_name": "minimal_order",
                    "metric_value": mean_order,
                    "instances_tested": n_tests,
                    "conjecture_holds": False,
                    "counterexample": f"Order {order} exceeds expected by more than 50%"
                }
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_order,
        "instances_tested": n_tests,
        "conjecture_holds": False,
        "counterexample": f"Not enough support (only {support_fraction:.2f})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    std_dev = (sum((result["metric_value"] - mean_order) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] > 1.5 * Fraction(n_tests * k, 2) * math.log(n_tests) for n_tests in range(5, 41)):
        print(f"RESULT: FALSIFIED counterexample=\"Order exceeds expected by more than 50%\" first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds'] and result['metric_value'] > 1.5 * Fraction(n_tests * k, 2) * math.log(n_tests)))]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")