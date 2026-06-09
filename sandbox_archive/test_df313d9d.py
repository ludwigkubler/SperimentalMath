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
    
    def tseitin_formula(n):
        clauses = []
        for i in range(1, n + 1):
            clauses.append([i])
            clauses.append([-i])
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append([i, -j])
                clauses.append([-i, j])
                clauses.append([j, -i])
                clauses.append([-j, i])
        return clauses
    
    def hamiltonian(clauses):
        n = len(clauses)
        H = [[0] * (2 * n) for _ in range(2 * n)]
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    row, col = literal - 1, literal + n - 1
                else:
                    row, col = -literal - 1, -literal - 1
                H[row][col] += 1
        return H
    
    def geometric_entropy(H):
        n = len(H)
        det_H = determinant(H)
        if det_H == 0:
            return float('inf')
        entropy = -math.log(abs(det_H)) / math.log(2)
        return entropy
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def frege_proof_width(clauses):
        n = len(clauses)
        width = 0
        for clause in clauses:
            width = max(width, len(clause))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi_G = tseitin_formula(n)
        H = hamiltonian(phi_G)
        mge_phi_G = geometric_entropy(H)
        w_phi_G = frege_proof_width(phi_G)
        
        if mge_phi_G == float('inf'):
            continue
        
        results.append({
            "n": n,
            "mge_phi_G": mge_phi_G,
            "w_phi_G": w_phi_G
        })
    
    if not results:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    mge_values = [result["mge_phi_G"] for result in results]
    w_values = [result["w_phi_G"] for result in results]
    
    mean_mge = sum(mge_values) / instances_tested
    std_mge = math.sqrt(sum((x - mean_mge) ** 2 for x in mge_values) / instances_tested)
    mean_w = sum(w_values) / instances_tested
    
    if all(abs(mge / w - 1) <= 0.1 for mge, w in zip(mge_values, w_values)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mge not within a factor of 10 of Frege proof width"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_mge,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mge not within a factor of 10 of Frege proof width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")