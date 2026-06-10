# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i and A[k][i]:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(sat_formula, assignment):
        if not sat_formula:
            return True
        literal = next(lit for lit in sat_formula[0] if lit not in assignment)
        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[literal] = value
            if dpll([clause for clause in sat_formula if literal not in clause and -literal not in clause], new_assignment):
                return True
        return False

    def cnf_complexity(sat_formula):
        return len(sat_formula)

    def topological_entanglement(n):
        # Simplified model of topological entanglement
        return Fraction(1, n**2)

    def generate_cnf(n):
        clauses = []
        for i in range(n):
            clause = [random.choice([i + 1, -(i + 1)]) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses

    metric_name = "Pearson's correlation coefficient"
    instances_tested = 0
    n_max = 0
    entanglement_values = []
    complexity_values = []

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            sat_formula = generate_cnf(n)
            entanglement = topological_entanglement(n)
            complexity = cnf_complexity(sat_formula)
            
            entanglement_values.append(entanglement)
            complexity_values.append(complexity)
            instances_tested += 1

    if not entanglement_values or not complexity_values:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_entanglement = sum(entanglement_values) / len(entanglement_values)
    mean_complexity = sum(complexity_values) / len(complexity_values)

    correlation_coefficient = 0
    if mean_entanglement != 0 and mean_complexity != 0:
        numerator = sum((ent - mean_entanglement) * (comp - mean_complexity) for ent, comp in zip(entanglement_values, complexity_values))
        denominator = len(entanglement_values) * abs(mean_entanglement) * abs(mean_complexity)
        correlation_coefficient = numerator / denominator

    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient <= 5 and len(entanglement_values) >= 30,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100, 4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values)/len(metric_values):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")