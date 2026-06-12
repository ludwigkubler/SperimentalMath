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
    
    def generate_boolean_formula(n):
        literals = [f'v{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            if random.choice([True, False]):
                clause[0] = f'~{clause[0]}'
            if random.choice([True, False]):
                clause[1] = f'~{clause[1]}'
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    def satisfiable_points(phi):
        n = len(phi) // (next(k for k in phi if k.startswith('v'))[1:])
        points = []
        for i in range(2**n):
            point = [bool(i & (1 << j)) for j in range(n)]
            if eval(phi, {'v': point}):
                points.append(point)
        return points
    
    def minimal_order(points):
        n = len(points[0])
        order = 0
        while True:
            covered = set()
            for point in points:
                if not any(point[i] == covered[i] for i in range(n)):
                    covered.add(tuple(point))
            if len(covered) == len(points):
                return order
            order += 1
    
    def resolution_proof_depth(phi):
        n = len(phi) // (next(k for k in phi if k.startswith('v'))[1:])
        clauses = phi.split(' and ')
        stack = []
        while True:
            if not clauses:
                return len(stack)
            clause = random.choice(clauses)
            if ' or ' in clause:
                literals = clause.split(' or ')
                if any(lit.startswith('~') for lit in literals):
                    continue
                stack.append(clause)
                break
            else:
                literal = clause
                if literal.startswith('~'):
                    continue
                stack.append(clause)
                break
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        phi = generate_boolean_formula(n)
        points = satisfiable_points(phi)
        if not points:
            continue
        omega_phi = minimal_order(points)
        d_phi = resolution_proof_depth(phi)
        results.append((omega_phi, d_phi))
    
    if len(results) < 30:
        return {
            "metric_name": "resolution_proof_depth",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_points"
        }
    
    omega_phi_values = [omega for omega, _ in results]
    d_phi_values = [d for _, d in results]
    
    correlation_coefficient = sum((omega - mean_omega) * (d - mean_d) for omega, d in results)
    correlation_coefficient /= math.sqrt(sum((omega - mean_omega)**2 for omega in omega_phi_values)) * math.sqrt(sum((d - mean_d)**2 for d in d_phi_values))
    
    mean_difference = sum(abs(omega - d) for omega, d in results) / len(results)
    
    return {
        "metric_name": "resolution_proof_depth",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_difference <= 3,
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
    
    mean_correlation_coefficient = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_correlation_coefficient)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation_coefficient} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")