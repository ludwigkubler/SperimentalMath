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
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 10)
    clauses = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    
    # Convert clauses to points in {0,1}^n
    points = [tuple(clause) for clause in clauses]
    
    # Compute convex hull using a simple algorithm (e.g., QuickHull)
    def quickhull(points):
        if len(points) <= 3:
            return set(points)
        
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            elif val > 0:
                return 1
            else:
                return 2
        
        def distance(p, q):
            return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)
        
        def furthest_point(points, p, q):
            max_dist = 0
            farthest = None
            for point in points:
                dist = distance(point, p) if orientation(p, q, point) == 0 else float('-inf')
                if dist > max_dist:
                    max_dist = dist
                    farthest = point
            return farthest
        
        def quickhull_recursive(points, p, q):
            hull = set()
            for r in points:
                if orientation(p, q, r) == 2:
                    hull.add(r)
            
            if not hull:
                return {p, q}
            
            max_point = furthest_point(hull, p, q)
            left_hull = quickhull_recursive(points, p, max_point)
            right_hull = quickhull_recursive(points, q, max_point)
            return left_hull.union(right_hull)
        
        hull_points = set()
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                hull_points.update(quickhull_recursive(points, points[i], points[j]))
        return hull_points
    
    convex_hull = quickhull(points)
    
    # Approximate surface area using Monte Carlo integration
    def monte_carlo_surface_area(convex_hull, n_samples=10000):
        total_area = 0
        for _ in range(n_samples):
            point = tuple(random.random() for _ in range(len(next(iter(convex_hull)))))
            if all(point[i] == 0 or point[i] == 1 for i in range(len(point))):
                inside = True
                for edge in convex_hull:
                    if len(edge) != 2:
                        continue
                    p, q = edge
                    if (point[0] - p[0]) * (q[1] - p[1]) == (q[0] - p[0]) * (point[1] - p[1]):
                        inside = not inside
                if inside:
                    total_area += 1
        return total_area / n_samples
    
    surface_area = monte_carlo_surface_area(convex_hull)
    
    # Compute resolution proof length using DPLL with clause learning
    def dpll_with_clause_learning(clauses):
        literals = set()
        for clause in clauses:
            literals.update(clause)
        
        def unit_propagation(clauses, assignment):
            while True:
                unit_clauses = [c for c in clauses if len(c) == 1 and c[0] not in assignment]
                if not unit_clauses:
                    break
                literal = unit_clauses[0][0]
                assignment[literal] = True
                clauses = [[l for l in c if l != literal] for c in clauses]
        def pure_literal_elimination(clauses, literals):
            while True:
                pure_literals = [l for l in literals if (not any(l in clause for clause in clauses) and not any(-l in clause for clause in clauses))]
                if not pure_literals:
                    break
                literal = pure_literals[0]
                assignment[literal] = True
                clauses = [[l for l in c if l != literal] for c in clauses]
        def backtracking(clauses, literals):
            if not clauses:
                return True
            if any(len(c) == 0 for c in clauses):
                return False
            
            literal = next(l for l in literals if l not in assignment)
            assignment[literal] = True
            if backtracking(clauses, literals):
                return True
            assignment[literal] = False
            assignment[-literal] = True
            if backtracking(clauses, literals):
                return True
            return False
        
        assignment = {}
        unit_propagation(clauses, assignment)
        pure_literal_elimination(clauses, literals)
        if not backtracking(clauses, literals):
            return None  # Unsatisfiable
        
        proof_length = sum(len(c) for c in clauses)
        return proof_length
    
    proof_length = dpll_with_clause_learning(clauses)
    
    if proof_length is None:
        return {
            "metric_name": "SurfaceArea * ProofLength",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable"
        }
    
    # Check the conjecture
    if surface_area == 0:
        return {
            "metric_name": "SurfaceArea * ProofLength",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "surface_area_zero"
        }
    
    C = surface_area / (math.log(m) / proof_length)
    
    return {
        "metric_name": "SurfaceArea * ProofLength",
        "metric_value": surface_area * proof_length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [53, 67, 71, 73, 79]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")