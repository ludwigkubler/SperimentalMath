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

# Define permutations as tuples (e.g., (1, 2, 3, 4, 5))
a = (1, 2, 3, 4, 5)
b = (1, 3, 5, 2, 4)

def compose(p1, p2):
    return tuple(p1[p2[i] - 1] for i in range(5))

def inverse(p):
    return tuple(p.index(i + 1) + 1 for i in range(5))

def perm_matrix(p):
    M = [[0] * 5 for _ in range(5)]
    for i, j in enumerate(p):
        M[i][j - 1] = 1
    return M

def frobenius_norm(M):
    return math.sqrt(sum(x**2 for row in M for x in row))

def Barrington_AND(n):
    if n == 2:
        return [(1, a, b), (2, b, a)]
    else:
        subprogram = Barrington_AND(n // 2)
        new_program = []
        for literal_index, perm_for_x0, perm_for_x1 in subprogram:
            new_perm_for_x0 = compose(a, perm_for_x0) if literal_index % 2 == 0 else inverse(compose(a, perm_for_x0))
            new_perm_for_x1 = compose(b, perm_for_x1) if literal_index % 2 == 0 else inverse(compose(b, perm_for_x1))
            new_program.append((literal_index * 2 + 1, new_perm_for_x0, new_perm_for_x1))
        return new_program

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 8, 16, 32]
    results = []
    
    for n in n_values:
        L_n = n ** 2
        total_defect = 0
        
        for _ in range(30):
            x = tuple(random.randint(0, 1) for _ in range(n))
            prefix_products = [a] * (n + 1)
            
            for literal_index, perm_for_x0, perm_for_x1 in Barrington_AND(n):
                if x[literal_index - 1] == 0:
                    prefix_products.append(perm_for_x0)
                else:
                    prefix_products.append(perm_for_x1)
            
            M_bar = sum(perm_matrix(p) for p in prefix_products[1:]) / L_n
            J = [[Fraction(1, 5)] * 5 for _ in range(5)]
            defect = frobenius_norm([M_bar[i][j] - J[i][j] for i in range(5) for j in range(5)])
            total_defect += defect
        
        avg_defect = total_defect / 30
        results.append(avg_defect)
    
    D_bar_values = [results[0]]
    slopes = []
    
    for i in range(1, len(results)):
        slope = math.log2(results[i - 1] / results[i])
        if not (0.5 < slope < 3.0):
            return {
                "metric_name": "D_bar",
                "metric_value": None,
                "instances_tested": 4 * 30,
                "conjecture_holds": False,
                "counterexample": f"slope_{n_values[i]}={slope}"
            }
        D_bar_values.append(results[i])
        slopes.append(slope)
    
    if all(D_bar_values[i] > D_bar_values[i + 1] for i in range(len(D_bar_values) - 1)):
        return {
            "metric_name": "D_bar",
            "metric_value": None,
            "instances_tested": 4 * 30,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "D_bar",
            "metric_value": None,
            "instances_tested": 4 * 30,
            "conjecture_holds": False,
            "counterexample": "monotonicity_failed"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    all_results = []
    total_defects = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        all_results.append(trial_result["metric_value"])
        if trial_result["conjecture_holds"]:
            count_supporting += 1
        
        total_defects += sum(all_results) / len(all_results)
    
    mean_defect = total_defects / len(seeds)
    support_fraction = count_supporting / len(seeds)
    
    if all(r is not None for r in all_results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_defect} std=0 support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='monotonicity_failed' first_failing_seed={seeds[count_supporting]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")