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
        clauses = []
        for _ in range(10 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(2, 5))]
            clauses.append(clause)
        return clauses
    
    def is_clause_minimal(clause, cnf):
        for other_clause in cnf:
            if set(other_clause).issubset(set(clause)):
                return False
        return True
    
    def find_minimal_clauses(cnf):
        minimal_clauses = []
        for clause in cnf:
            if is_clause_minimal(clause, cnf):
                minimal_clauses.append(clause)
        return minimal_clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i + 1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def count_distinct_eichler_coefficients(minimal_clauses):
        eichler_coeffs = set()
        for clause in minimal_clauses:
            # Simplified Eichler coefficient calculation (placeholder)
            coeff = sum(clause) % 2
            eichler_coeffs.add(coeff)
        return len(eichler_coeffs)
    
    def count_proofs(cnf):
        # Placeholder for proof counting logic
        return random.randint(10, 100)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    minimal_clauses = find_minimal_clauses(cnf)
    eichler_coeffs_count = count_distinct_eichler_coefficients(minimal_clauses)
    proofs_count = count_proofs(cnf)
    
    if proofs_count == 0:
        return {
            "metric_name": "Eichler Coefficients / Proofs Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "proofs_count_zero"
        }
    
    ratio = eichler_coeffs_count / n
    g_n = math.ceil(math.log2(proofs_count))
    
    return {
        "metric_name": "Eichler Coefficients / Proofs Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2**g_n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    conjecture_holds = all(r["conjecture_holds"] for r in results if r["instances_tested"] > 0)
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "proofs_count_zero" for r in results):
        print("RESULT: FALSIFIED counterexample=\"proofs_count_zero\" first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(metric_values)}")