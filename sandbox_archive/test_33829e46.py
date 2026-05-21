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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def generate_d_regular_expander(n, d):
        if (n * (d - 1)) % 2 != 0:
            raise ValueError("Invalid parameters for expander graph")
        edges = set()
        while len(edges) < n * (d - 1) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return edges
    
    def tseitin_formula(edges):
        clauses = []
        literals = {}
        var_id = 0
        for u, v in edges:
            if u not in literals:
                literals[u] = var_id
                var_id += 1
            if v not in literals:
                literals[v] = var_id
                var_id += 1
            clauses.append((literals[u], -literals[v]))
            clauses.append((-literals[u], literals[v]))
        return clauses
    
    def polynomial_system(clauses):
        variables = set()
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    variables.add(literal)
        polynomials = []
        for var in variables:
            poly = [1]
            for clause in clauses:
                term = 1
                for literal in clause:
                    if literal == var:
                        term *= -1
                    elif literal < 0 and -literal in variables:
                        term *= (1 + random.choice([0, 1]))
                polynomials.append(poly)
        return polynomials
    
    def algebraic_degree(polynomials):
        degree = 0
        for poly in polynomials:
            degree = max(degree, len(poly) - 1)
        return degree
    
    def resolution_width(clauses):
        refutation_size = 0
        while clauses:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            clauses.remove(unit_clause)
            for clause in clauses:
                if literal in clause:
                    clause.remove(literal)
                elif -literal in clause:
                    clauses.remove(clause)
                    refutation_size += 1
        return refutation_size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(3, min(n - 1, 6))
        edges = generate_d_regular_expander(n, d)
        clauses = tseitin_formula(edges)
        polynomials = polynomial_system(clauses)
        degree = algebraic_degree(polynomials)
        width = resolution_width(clauses)
        results.append({"n": n, "degree": degree, "width": width})
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    degree_avg = sum(result["degree"] for result in results) / len(results)
    width_avg = sum(result["width"] for result in results) / len(results)
    
    if degree_avg >= width_avg:
        return {
            "metric_name": "resolution_width",
            "metric_value": width_avg,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "resolution_width",
            "metric_value": width_avg,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Degree {degree_avg} < Width {width_avg}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    degrees = [r["metric_value"] for r in all_results if r["conjecture_holds"]]
    widths = [r["metric_value"] for r in all_results]
    
    support_fraction = len(degrees) / len(all_results)
    mean_degree = sum(degrees) / len(degrees) if degrees else None
    std_degree = (sum((d - mean_degree)**2 for d in degrees) / len(degrees))**0.5 if degrees else None
    
    if all(r["conjecture_holds"] for r in all_results):
        print(f"RESULT: SUPPORTED mean={mean_degree} std={std_degree} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_degree} std={std_degree} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in all_results if not r["conjecture_holds"]), None)
        counterexample = f"Degree < Width at seed {first_failing_seed}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")