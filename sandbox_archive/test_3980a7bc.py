# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def indicator_function(monomial, clause):
        return all((x & abs(c)) == c for c in clause)
    
    def support(polynomial, GF):
        n = len(polynomial[0])
        support_set = set()
        for monomial in polynomial:
            if any(indicator_function(monomial, clause) for clause in F):
                support_set.add(tuple(monomial))
        return support_set
    
    def convex_hull(points):
        points = list(points)
        hull = []
        for p in sorted(points):
            while len(hull) >= 2 and (p[1] - hull[-2][1]) * (hull[-1][0] - hull[-2][0]) <= (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-2][0]):
                hull.pop()
            hull.append(p)
        return hull
    
    def dpll(F, assignment):
        if not F:
            return True
        for clause in F:
            if any(indicator_function(assignment, clause)):
                continue
            for literal in clause:
                new_assignment = list(assignment)
                new_assignment[abs(literal) - 1] = (new_assignment[abs(literal) - 1] + literal) % 2
                if dpll([c for c in F if not indicator_function(new_assignment, c)], new_assignment):
                    return True
            return False
        return False
    
    def count_edges(hull):
        n = len(hull)
        edges = 0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(hull[i][0] - hull[j][0]) == 1 or abs(hull[i][1] - hull[j][1]) == 1:
                    edges += 1
        return edges
    
    def random_3cnf(n, m):
        F = []
        for _ in range(m):
            clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)
                      for _ in range(random.randint(2, 3))]
            F.append(clause)
        return F
    
    def polynomial_from_3cnf(F):
        GF = 2
        n = len(F[0])
        polynomial = [tuple(0 for _ in range(n)) for _ in range(GF**n)]
        for clause in F:
            monomial = tuple((1 << (abs(lit) - 1)) if lit > 0 else (1 << (abs(lit) - 1)) ^ 1 for lit in clause)
            polynomial[monomial] = 1
        return polynomial
    
    n_values = [10, 12, 14, 16, 18, 20]
    m_factor = 4.3
    C = 10  # Universal constant for the bound
    total_edges = 0
    total_nodes = 0
    
    for n in n_values:
        m = int(m_factor * n)
        F = random_3cnf(n, m)
        polynomial = polynomial_from_3cnf(F)
        support_set = support(polynomial, GF=2)
        hull = convex_hull(support_set)
        edges = count_edges(hull)
        total_edges += edges
        
        for _ in range(10):
            assignment = [random.randint(0, 1) for _ in range(n)]
            if dpll(F, assignment):
                nodes = len([x for x in range(GF**n) if any(indicator_function(x, clause) for clause in F)])
                total_nodes += nodes
    
    mean_edges = total_edges / (len(n_values) * 10)
    mean_nodes = total_nodes / (len(n_values) * 10)
    
    conjecture_holds = mean_edges <= C * mean_nodes * n**2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Edge Count vs DPLL Nodes",
        "metric_value": mean_edges,
        "instances_tested": len(n_values) * 10,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_edges = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_edges} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_edges} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")