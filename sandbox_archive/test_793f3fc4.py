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
    
    def generate_sat_instance(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tseitin_transform(clauses, n):
        literals = set()
        for clause in clauses:
            for lit in clause:
                literals.add(abs(lit))
        m = len(clauses)
        new_vars = [n + i + 1 for i in range(m)]
        
        formula = []
        for i, clause in enumerate(clauses):
            for lit in clause:
                if lit > 0:
                    formula.append((lit, new_vars[i]))
                else:
                    formula.append((-lit, -new_vars[i]))
            formula.append((new_vars[i],))
        
        return literals, formula
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        m, n = len(A), len(A[0])
        A_rref = gaussian_elimination(A)
        rank = 0
        for row in A_rref:
            if any(row):
                rank += 1
        return rank
    
    def monodromy_group_order(n, m):
        literals, formula = tseitin_transform(generate_sat_instance(n, m), n)
        T = [[0] * (n + m) for _ in range(n + m)]
        for lit, new_var in formula:
            if lit > 0:
                T[lit - 1][new_var - 1] += 1
            else:
                T[-lit - 1][-new_var - 1] += 1
        return rank(T)
    
    def resolution_proof_width(clauses):
        stack = []
        for clause in clauses:
            stack.append(clause)
        
        while stack:
            clause1 = stack.pop()
            if not any(lit > 0 for lit in clause1):
                continue
            for clause2 in stack:
                if not any(lit < 0 for lit in clause2):
                    continue
                new_clause = []
                for lit1 in clause1:
                    if -lit1 in clause2:
                        break
                    else:
                        new_clause.append(lit1)
                for lit2 in clause2:
                    if lit2 > 0 and lit2 not in new_clause:
                        new_clause.append(-lit2)
                if len(new_clause) == 0:
                    return float('inf')
                stack.append(new_clause)
        
        return len(stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n, 2 * n)
            order = monodromy_group_order(n, m)
            width = resolution_proof_width(generate_sat_instance(n, m))
            results.append((order, width))
    
    if len(results) < 30:
        return {
            "metric_name": "monodromy_group_order",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    orders, widths = zip(*results)
    alpha = sum(order * width for order, width in results) / sum(width ** 2 for width in widths)
    correlation = sum((order - alpha * width) ** 2 for order, width in results) / len(results)
    
    return {
        "metric_name": "monodromy_group_order",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation < 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r and r["counterexample"])
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")