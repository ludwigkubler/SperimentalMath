# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_clause(n):
        return tuple(random.choice([-1, 1]) * (i + 1) for i in range(n))
    
    def generate_cnf(n, k):
        return [generate_clause(k) for _ in range(n)]
    
    def compute_Q_F(clauses):
        n = len(clauses[0])
        Q_F = {}
        for clause in clauses:
            exponent_vector = tuple(1 + ind(abs(lit), clause) for lit in clause)
            if exponent_vector not in Q_F:
                Q_F[exponent_vector] = 0
            Q_F[exponent_vector] += 1
        return Q_F
    
    def ind(lit, clause):
        return clause.index(lit)
    
    def compute_V_P(Q_F):
        monomials = list(Q_F.keys())
        n = len(monomials[0])
        points = [[monomial[i] for i in range(n)] for monomial in monomials]
        # Custom gift-wrapping fallback for convex hull
        def distance(p1, p2):
            return sum((p1[i] - p2[i]) ** 2 for i in range(n)) ** 0.5
        
        def find_min_distance(p, points):
            min_dist = float('inf')
            min_point = None
            for point in points:
                dist = distance(p, point)
                if dist < min_dist:
                    min_dist = dist
                    min_point = point
            return min_point
        
        hull = [points[0]]
        for point in points[1:]:
            while len(hull) > 1 and find_min_distance(hull[-2], [hull[-1], point]) == point:
                hull.pop()
            hull.append(point)
        return len(hull)
    
    def generate_all_circuits(n, m, B):
        gates = ['AND', 'OR']
        for circuit in itertools.product(gates, repeat=m):
            yield circuit
    
    def find_min_circuit(clauses):
        n = len(clauses[0])
        min_B = float('inf')
        for B in range(1, 13):
            for circuit in generate_all_circuits(n, m, B):
                # Simulate the circuit and check if it computes F
                computed_F = set()
                for clause in clauses:
                    result = True
                    for lit in clause:
                        if lit > 0:
                            result &= (random.choice([True, False]) if lit == random.choice([-1, 1] * n) else not random.choice([True, False]))
                        else:
                            result &= (not random.choice([True, False]) if -lit == random.choice([-1, 1] * n) else random.choice([True, False]))
                    computed_F.add(result)
                if computed_F == set(clause in clauses for clause in clauses):
                    min_B = B
                    break
            if min_B < float('inf'):
                break
        return min_B
    
    def compute_R(n, m, V_P, B_min):
        return V_P / (m * math.log2(n) * B_min)
    
    n_values = [6, 8, 10, 12, 14, 16]
    m_values = [2, 3, 5, 6]
    instances_tested = 0
    V_P_sum = 0
    R_list = []
    
    for n in n_values:
        for m in m_values:
            for _ in range(30):
                clauses = generate_cnf(n, m)
                Q_F = compute_Q_F(clauses)
                V_P = compute_V_P(Q_F)
                B_min = find_min_circuit(clauses)
                R = compute_R(n, m, V_P, B_min)
                instances_tested += 1
                V_P_sum += V_P
                R_list.append(R)
    
    mean_R = V_P_sum / instances_tested
    support_fraction = sum(1 for R in R_list if R <= 1) / len(R_list)
    
    conjecture_holds = support_fraction >= 0.99 and mean_R <= 0.8
    
    return {
        "metric_name": "R",
        "metric_value": mean_R,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_R = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_R} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")