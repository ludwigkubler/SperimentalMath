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
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            literals = [random.choice([1, -1]) * (i + 1) for i in random.sample(range(n), n)]
            clauses.append(literals)
        return clauses
    
    def compute_q_f(clauses):
        q_f = {}
        for clause in clauses:
            exp_vector = tuple(sorted(abs(lit) for lit in clause))
            if exp_vector not in q_f:
                q_f[exp_vector] = 0
            q_f[exp_vector] += 1
        return q_f
    
    def compute_v_p(q_f):
        monomials = list(q_f.keys())
        hull = convex_hull(monomials)
        return len(hull)
    
    def convex_hull(points):
        if len(points) <= 3:
            return points
        
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
        
        start = min(points, key=lambda p: (p[1], p[0]))
        points.remove(start)
        points.sort(key=lambda p: (math.atan2(p[1] - start[1], p[0] - start[0]), distance(p, start)))
        hull = [start]
        
        for point in points:
            while len(hull) > 1 and orientation(hull[-2], hull[-1], point) != 2:
                hull.pop()
            hull.append(point)
        
        return hull
    
    def find_min_circuit(clauses):
        n = len(clauses[0])
        m = len(clauses)
        B_min = float('inf')
        
        for B in range(1, 13):
            for circuit in generate_all_circuits(n, m, B):
                if evaluate_circuit(circuit, clauses) == True:
                    B_min = min(B_min, B)
                    break
            if B_min < float('inf'):
                break
        
        return B_min
    
    def generate_all_circuits(n, m, B):
        gates = ['AND', 'OR']
        for circuit in itertools.product(gates, repeat=m):
            yield circuit
    
    def evaluate_circuit(circuit, clauses):
        n = len(clauses[0])
        variables = [False] * n
        
        for clause in clauses:
            evaluated_clause = False
            for literal in clause:
                if literal > 0:
                    variables[literal - 1] = True
                else:
                    variables[-literal - 1] = False
            
            for gate, sub_circuit in zip(circuit, itertools.combinations(clauses, len(sub_circuit))):
                if gate == 'AND':
                    evaluated_clause &= all(evaluate_circuit(sub_circuit, clauses))
                elif gate == 'OR':
                    evaluated_clause |= any(evaluate_circuit(sub_circuit, clauses))
            
            if not evaluated_clause:
                return False
        
        return True
    
    n = random.randint(6, 16)
    k = random.randint(n, min(2 * n, 16))
    m = random.choice([2, 3, 5, 6])
    
    clauses = generate_k_cnf(n, k)
    q_f = compute_q_f(clauses)
    v_p = compute_v_p(q_f)
    
    B_min = find_min_circuit(clauses)
    
    if v_p > m * math.log2(n) * B_min:
        return {
            "metric_name": "R",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"V(P(F)) > m·log2(n)·B for n={n}, k={k}, m={m}"
        }
    
    return {
        "metric_name": "R",
        "metric_value": v_p / (m * math.log2(n) * B_min),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction=1.0")
    elif any(r["metric_value"] > 1 for r in results):
        first_failing_seed = next(seed for seed, r in enumerate(results) if r["metric_value"] > 1)
        print(f"RESULT: FALSIFIED counterexample='R > 1' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient data")