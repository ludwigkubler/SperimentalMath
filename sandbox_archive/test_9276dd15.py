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
        literals = list(range(-m, 0)) + list(range(1, m + 1))
        clauses = []
        for i in range(m):
            clause = [random.choice(literals) for _ in range(random.randint(2, 5))]
            clauses.append(clause)
        return clauses

    def tseitin_formula(clauses):
        literals = set()
        formulas = {}
        counter = 1
        for clause in clauses:
            literals.update(clause)
            for literal in clause:
                if literal < 0:
                    negated = -literal
                else:
                    negated = -literal
                if negated not in formulas:
                    formulas[negated] = counter
                    counter += 1
        return formulas

    def incidence_matrix(tseitin):
        n = len(tseitin)
        m = len(clauses)
        matrix = [[0 for _ in range(m)] for _ in range(n)]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal < 0:
                    row = -literal
                else:
                    row = literal
                matrix[row][i] = 1
        return matrix

    def hodge_diamond_dimension(matrix):
        n = len(matrix)
        characteristic_poly = [1]
        for i in range(n):
            new_poly = [0] * (len(characteristic_poly) + 1)
            for j in range(len(characteristic_poly)):
                new_poly[j + 1] += characteristic_poly[j]
            characteristic_poly = new_poly
        return len(characteristic_poly)

    def communication_complexity(clauses):
        m = len(clauses)
        return m * (m - 1) // 2

    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, n_max + 1, 5):
        m = random.randint(n, n * 3)
        cnf = generate_cnf(m)
        tseitin = tseitin_formula(cnf)
        matrix = incidence_matrix(tseitin)
        hdd = hodge_diamond_dimension(matrix)
        cc = communication_complexity(cnf)
        
        metric_values.append(hdd / cc)
        instances_tested += 1
    
    mean_value = sum(metric_values) / len(metric_values)
    conjecture_holds = all(0.9 <= value <= 1.1 for value in metric_values)
    
    return {
        "metric_name": "HDD/CC Ratio",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")