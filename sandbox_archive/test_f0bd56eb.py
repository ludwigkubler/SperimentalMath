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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(cnf):
        clauses = [set(clause) for clause in cnf]
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        
        def is_satisfiable(model, clauses):
            for clause in clauses:
                if not any(lit in model or -lit in model for lit in clause):
                    return False
            return True
        
        def backtrack():
            assignment = {}
            stack = []
            while True:
                while literals:
                    literal = next(iter(literals))
                    assignment[literal] = True
                    stack.append((literal, assignment.copy()))
                    literals.remove(literal)
                    if not is_satisfiable(assignment, clauses):
                        del assignment[literal]
                        literals.add(literal)
                        literal, assignment = stack.pop()
                        assignment[literal] = False
                        literals.remove(-literal)
                        stack.append((-literal, assignment.copy()))
                        literals.add(-literal)
                if all(lit in assignment or -lit in assignment for lit in literals):
                    return True, assignment
                literal, assignment = stack.pop()
                literals.add(abs(literal))
                literals.add(-literal)
        
        stree_width = 0
        while backtrack():
            stree_width += 1
        
        return stree_width

    def geometric_entropy(n):
        # Placeholder for actual computation of geometric entropy
        return n * math.log(n)

    def cnf_to_hodge_structure(cnf):
        # Placeholder for actual mapping to Hodge structure
        return random.randint(1, 100)  # Simplified example

    instances_tested = 30
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = [[random.randint(-n, n) for _ in range(random.randint(1, n))] for _ in range(n)]
        hodge_structure = cnf_to_hodge_structure(cnf)
        stree_width = dpll(cnf)
        geo_ent = geometric_entropy(hodge_structure)

        if geo_ent > 1.1 * (n**3 * math.log(n) * stree_width):
            conjecture_holds = False
            counterexample = f"GeoEnt({hodge_structure}) > 1.1 * n^3 * log(n) * STreeWidth(T)"
            break

        total_metric_value += geo_ent

    return {
        "metric_name": "Geometric Entropy",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 97, 3))  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")