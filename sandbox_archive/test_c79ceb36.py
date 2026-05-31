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
    
    def generate_cnf(m):
        cnf = []
        for i in range(m):
            clause = [random.randint(1, 2*m) for _ in range(random.randint(3, 5))]
            cnf.append(clause)
        return cnf
    
    def tseitin_formula(cnf):
        literals = set()
        for clause in cnf:
            literals.update(clause)
        n = len(literals)
        
        tseitin = []
        var_count = 2 * n + m
        for i, clause in enumerate(cnf):
            literal = var_count + i + 1
            tseitin.append([literal] + [-l for l in clause])
            for l in clause:
                tseitin.append([-literal, -l])
        
        return tseitin
    
    def incidence_matrix(tseitin):
        n = len(tseitin)
        m = len(tseitin[0]) - 1
        matrix = [[0] * (n + m) for _ in range(n)]
        for i, clause in enumerate(tseitin):
            literal = clause[-1]
            for l in clause[:-1]:
                if l > 0:
                    row = literals.index(l)
                else:
                    row = literals.index(-l) + n
                matrix[row][literal - 1] = 1
        return matrix
    
    def hodge_diamond_dimension(matrix):
        n = len(matrix)
        char_poly = [Fraction(1)]
        for i in range(n):
            char_poly = [sum(char_poly[j] * matrix[i][j] for j in range(i + 1)) for _ in range(len(char_poly))]
        return sum(abs(coeff) for coeff in char_poly)
    
    def communication_complexity(cnf):
        m = len(cnf)
        n = max(max(clause) for clause in cnf)
        return m * (n + 1)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            if matrix[i][i] == 0:
                for j in range(i + 1, rows):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None
            pivot = Fraction(matrix[i][i])
            for j in range(cols):
                matrix[i][j] /= pivot
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        matrix = gaussian_elimination(matrix)
        if matrix is None:
            return 0
        return sum(1 for row in matrix if any(coeff != 0 for coeff in row))
    
    m_values = [5, 10, 15, 20, 30, 40]
    hdd_values = []
    cc_values = []
    
    for m in m_values:
        cnf = generate_cnf(m)
        tseitin = tseitin_formula(cnf)
        matrix = incidence_matrix(tseitin)
        hdd = hodge_diamond_dimension(matrix)
        cc = communication_complexity(cnf)
        hdd_values.append(hdd)
        cc_values.append(cc)
    
    if len(hdd_values) < 30:
        return {
            "metric_name": "HDD vs CC",
            "metric_value": None,
            "instances_tested": len(hdd_values),
            "n_max": max(m_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_hdd = sum(hdd_values) / len(hdd_values)
    std_hdd = math.sqrt(sum((hdd - mean_hdd) ** 2 for hdd in hdd_values) / len(hdd_values))
    mean_cc = sum(cc_values) / len(cc_values)
    std_cc = math.sqrt(sum((cc - mean_cc) ** 2 for cc in cc_values) / len(cc_values))
    
    correlation_coefficient = sum((hdd - mean_hdd) * (cc - mean_cc) for hdd, cc in zip(hdd_values, cc_values)) / (len(hdd_values) * std_hdd * std_cc)
    
    return {
        "metric_name": "HDD vs CC",
        "metric_value": correlation_coefficient,
        "instances_tested": len(hdd_values),
        "n_max": max(m_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.9 and p_value <= 0.01,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ranks = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_ranks = math.sqrt(sum((result["metric_value"] - mean_ranks) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ranks} std={std_ranks} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ranks} std={std_ranks} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")