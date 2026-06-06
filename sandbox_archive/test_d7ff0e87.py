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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def tropical_curve(cnf):
        # Simplified mapping: each literal is a point on the tropical projective line
        points = set()
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    points.add((lit, 1))
                else:
                    points.add((-lit, -1))
        return points
    
    def order_of_singularity(points):
        # Simplified calculation: number of distinct points
        return len(points)
    
    def resolution_proof_width(cnf):
        # Small DPLL solver implementation
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
                new_assignment[literal] = False
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
            else:
                literal = next((i + 1 for i, (a, b) in enumerate(assignment.items()) if a is None), None)
                if literal is None:
                    return False
                assignment[literal] = True
                if dpll(clauses, assignment):
                    return True
                assignment[literal] = False
                if dpll(clauses, assignment):
                    return True
            return False
        
        def count_conflicts(assignment):
            conflicts = 0
            for clause in cnf:
                satisfied = any(lit in assignment and assignment[lit] == (lit > 0) for lit in clause)
                if not satisfied:
                    conflicts += 1
            return conflicts
        
        width = 0
        while True:
            assignment = {i + 1: None for i in range(len(cnf))}
            if dpll(cnf, assignment):
                break
            width += 1
        return width
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = (sum((x[i] - mean_x) ** 2 for i in range(n)) / n) ** 0.5
        std_y = (sum((y[i] - mean_y) ** 2 for i in range(n)) / n) ** 0.5
        return cov_xy / (std_x * std_y)
    
    def p_value(r, n):
        if r == 1:
            return 0
        t_stat = r * ((n - 2) / (1 - r**2))**0.5
        df = n - 2
        # Approximate p-value using normal distribution
        from math import erf
        p = 2 * (1 - 0.5 * erf(abs(t_stat) / (2 ** 0.5)))
        return p
    
    m = random.randint(1, 40)
    n = random.randint(1, 40)
    cnf = generate_cnf(m, n)
    
    points = tropical_curve(cnf)
    o_C_phi = order_of_singularity(points)
    w_phi = resolution_proof_width(cnf)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient([o_C_phi], [w_phi]),
        "instances_tested": 1,
        "n_max": max(m, n),
        "conjecture_holds": correlation_coefficient([o_C_phi], [w_phi]) > 0.7 and p_value(correlation_coefficient([o_C_phi], [w_phi]), 2) < 0.05,
        "counterexample": "" if correlation_coefficient([o_C_phi], [w_phi]) > 0.3 and p_value(correlation_coefficient([o_C_phi], [w_phi]), 2) < 0.05 else "Correlation too weak or p-value too high"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [random.randint(1, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] <= 0.3 or p_value(r["metric_value"], 2) >= 0.05 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too weak or p-value too high\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'] and r['metric_value'] <= 0.3 or p_value(r['metric_value'], 2) >= 0.05)]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")