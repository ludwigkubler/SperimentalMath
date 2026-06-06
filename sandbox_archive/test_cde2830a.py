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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def tropical_curve(cnf):
        # Convert CNF to a list of points on the tropical projective line
        points = []
        for clause in cnf:
            point = [sum(abs(lit) for lit in clause), 1]
            points.append(point)
        return points
    
    def order_of_singularity(points):
        # Compute the intersection multiplicity of curve singularities
        n = len(points)
        if n < 2:
            return 0
        
        def determinant(matrix):
            if len(matrix) == 2:
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            det = 0
            for i in range(len(matrix)):
                submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
                det += (-1) ** i * matrix[0][i] * determinant(submatrix)
            return det
        
        order = 0
        for i in range(n):
            for j in range(i + 1, n):
                matrix = [[points[i][0], points[j][0]], [points[i][1], points[j][1]]]
                if determinant(matrix) == 0:
                    order += 1
        return order
    
    def resolution_width(cnf):
        # Implement a small DPLL solver to determine the resolution proof width
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal in assignment and assignment[literal] != (literal > 0):
                    return False
                new_assignment = assignment.copy()
                new_assignment[literal] = True if literal > 0 else False
                return dpll([c for c in clauses if literal not in c], new_assignment)
            pure_literal = next((l for l in range(1, len(clauses[0]) + 1) if (l not in assignment and -l not in assignment)), None)
            if pure_literal:
                new_assignment = assignment.copy()
                new_assignment[pure_literal] = True
                return dpll([c for c in clauses if pure_literal not in c], new_assignment)
            literal, _ = random.choice(clauses)
            if literal > 0:
                return dpll(clauses, {**assignment, literal: True}) or dpll(clauses, {**assignment, literal: False})
            else:
                return dpll(clauses, {**assignment, -literal: True}) or dpll(clauses, {**assignment, -literal: False})
        
        assignment = {}
        if not dpll(cnf, assignment):
            return 0
        
        def resolve(clause1, clause2):
            resolved_clause = [l for l in clause1 if l not in clause2 and -l not in clause2]
            return resolved_clause
        
        resolution_steps = []
        while True:
            new_clauses = set()
            for i in range(len(cnf)):
                for j in range(i + 1, len(cnf)):
                    if any(lit in cnf[i] and -lit in cnf[j] for lit in cnf[i]):
                        resolved_clause = resolve(cnf[i], cnf[j])
                        new_clauses.add(tuple(sorted(resolved_clause)))
            if not new_clauses:
                break
            resolution_steps.extend(new_clauses)
            cnf.extend(list(new_clauses))
        
        return len(resolution_steps)
    
    n_max = 0
    instances_tested = 0
    total_order = 0
    total_width = 0
    
    for m in range(1, 41):
        for n in range(1, 41 - m + 1):
            if m + n > 40:
                continue
            
            cnf = generate_cnf(m, n)
            points = tropical_curve(cnf)
            order = order_of_singularity(points)
            width = resolution_width(cnf)
            
            total_order += order
            total_width += width
            instances_tested += 1
            n_max = max(n_max, m + n)
    
    if instances_tested == 0:
        return {
            "metric_name": "Order of Singularities vs Resolution Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * sum(order * width for order, width in zip(range(1, instances_tested + 1), range(1, instances_tested + 1))) - instances_tested * mean_order * mean_width) / math.sqrt((instances_tested * sum(order ** 2 for order in range(1, instances_tested + 1)) - instances_tested * mean_order ** 2) * (instances_tested * sum(width ** 2 for width in range(1, instances_tested + 1)) - instances_tested * mean_width ** 2))
    
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(instances_tested - 2)))
    
    return {
        "metric_name": "Order of Singularities vs Resolution Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7 and p_value < 0.05,
        "counterexample": "" if correlation_coefficient > 0.7 and p_value < 0.05 else f"Correlation: {correlation_coefficient}, P-value: {p_value}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif any(not r["conjecture_holds"] and r["metric_value"] <= 0.3 or r["p_value"] >= 0.05 for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")