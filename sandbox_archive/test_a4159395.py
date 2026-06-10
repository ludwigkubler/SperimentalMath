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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
        pure_literals = [l for l in range(1, n + 1) if all(l not in c or -l not in c for c in cnf)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
        literals = [l for l in range(1, n + 1) if l not in assignment and -l not in assignment]
        literal = literals[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        return False
    
    def algebraic_automorphism_group(cnf):
        n = len(cnf)
        generators = []
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if all((i in c or -i in c) == (j in c or -j in c) for c in cnf):
                    generators.append((i, j))
        return generators
    
    def rank(generators):
        m = len(generators)
        n = len(set([abs(x) for x in sum(generators, [])]))
        A = [[0] * n for _ in range(m)]
        for i, (a, b) in enumerate(generators):
            A[i][abs(a) - 1] += 1
            A[i][abs(b) - 1] += 1
        rank = 0
        for i in range(n):
            if any(A[j][i] != 0 for j in range(rank)):
                for j in range(rank, m):
                    if A[j][i] != 0:
                        A[j], A[rank] = A[rank], A[j]
                        break
                for j in range(m):
                    if j != rank and A[j][i] != 0:
                        factor = A[j][i] / A[rank][i]
                        for k in range(n):
                            A[j][k] -= factor * A[rank][k]
                rank += 1
        return rank
    
    def circuit_satisfiability_complexity(cnf):
        n = len(cnf)
        assignment = {}
        if dpll(cnf, assignment):
            return 0
        else:
            return float('inf')
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            generators = algebraic_automorphism_group(cnf)
            r = rank(generators)
            c = circuit_satisfiability_complexity(cnf)
            results.append((r, c))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = sum((r - r_mean) * (c - c_mean) for r, c in results) / math.sqrt(sum((r - r_mean)**2 for r, _ in results) * sum((c - c_mean)**2 for _, c in results))
    r_mean = sum(r for r, _ in results) / len(results)
    c_mean = sum(c for _, c in results) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) > 0.8 and correlation_coefficient <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) > 0.8 and r["metric_value"] <= 3) / len(results)
    
    if all(abs(r["metric_value"]) > 0.8 and r["metric_value"] <= 3 for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(abs(r["metric_value"]) > 0.8 and r["metric_value"] <= 3 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={seeds[results.index(next(r for r in results if abs(r['metric_value']) > 0.8 and r['metric_value'] <= 3))]}")
    else:
        print("RESULT: INCONCLUSIVE no_positive_correlation_or_metric_saturation")