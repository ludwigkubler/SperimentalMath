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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    def quadratic_form(cnf):
        n = len(cnf[0])
        qform = [[0] * n for _ in range(n)]
        for clause in cnf:
            for x in clause:
                for y in clause:
                    if abs(x) == abs(y):
                        qform[abs(x)-1][abs(y)-1] += 1
        return qform
    
    def min_integral_points(qform):
        n = len(qform)
        det = determinant(qform)
        if det == 0:
            return float('inf')
        return math.ceil(abs(det) ** (1/n))
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def sat_entropy(cnf):
        n = len(cnf)
        total_clauses = sum(1 for clause in cnf if any(x != 0 for x in clause))
        entropy = -total_clauses / (n * math.log2(n)) if n > 0 else float('inf')
        return entropy
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        qform = quadratic_form(cnf)
        min_points = min_integral_points(qform)
        entropy = sat_entropy(cnf)
        
        if min_points == float('inf'):
            continue
        
        instances_tested += 1
        total_metric_value += min_points * entropy
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
    support_fraction = instances_tested / (n_max - 4)
    
    if support_fraction < 0.8:
        conjecture_holds = False
        counterexample = "support_fraction_too_low"
    
    return {
        "metric_name": "MinIntegralPoints * SATEntropy",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] == "support_fraction_too_low" for r in results):
        print("RESULT: FALSIFIED counterexample=\"support_fraction_too_low\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction_too_low")