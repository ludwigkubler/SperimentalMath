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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def hamiltonian_matrix(cnf):
        n = max(abs(lit) for lit in cnf)
        H = [[0] * (2 * n + 1) for _ in range(2 * n + 1)]
        
        for clause in cnf:
            x, y = abs(clause[0]), abs(clause[1])
            if clause[0] > 0:
                i = x
            else:
                i = -x
            if clause[1] > 0:
                j = y
            else:
                j = -y
            H[i][j] += 1
            H[j][i] += 1
        
        return H
    
    def min_quaternionic_norm(H):
        n = len(H)
        det = determinant(H)
        if det == 0:
            raise ValueError("Singular matrix")
        norm = abs(det) ** (Fraction(1, n))
        return norm
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def monotone_width(cnf):
        n = max(abs(lit) for lit in cnf)
        circuit = []
        
        for clause in cnf:
            if clause[0] > 0 and clause[1] < 0:
                circuit.append((clause[0], -clause[1]))
            elif clause[0] < 0 and clause[1] > 0:
                circuit.append((-clause[0], clause[1]))
        
        width = len(circuit)
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_norm = Fraction(0)
    total_width = Fraction(0)
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, n * (n - 1) // 2)
            try:
                H = hamiltonian_matrix(cnf)
                norm = min_quaternionic_norm(H)
                width = monotone_width(cnf)
                
                total_norm += norm
                total_width += width
                instances_tested += 1
            except ValueError as e:
                return {
                    "metric_name": "correlation",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
    
    mean_norm = total_norm / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (mean_norm * mean_width) / (instances_tested - 1)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")