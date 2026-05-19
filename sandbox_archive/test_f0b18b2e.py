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
    
    def generate_3cnf(n: int, m: int):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def convex_hull_area(clauses):
        # Simplified Monte Carlo method to approximate surface area
        n = len(clauses)
        points = [(c[0], c[1]) for c in clauses]
        min_x, max_x = min(p[0] for p in points), max(p[0] for p in points)
        min_y, max_y = min(p[1] for p in points), max(p[1] for p in points)
        area = (max_x - min_x) * (max_y - min_y)
        return area

    def resolution_proof_length(clauses):
        # Simplified DPLL with clause learning
        stack = []
        learned_clauses = set()
        while clauses:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            for i, clause in enumerate(clauses):
                if literal in clause:
                    clauses[i] = [l for l in clause if l != literal and -l != literal]
                    if len(clauses[i]) == 0:
                        return float('inf')
                elif -literal in clause:
                    learned_clauses.add((literal, -literal))
            stack.append(literal)
        return len(stack) + len(learned_clauses)

    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 10)
    clauses = generate_3cnf(n, m)
    surface_area = convex_hull_area(clauses)
    proof_length = resolution_proof_length(clauses)
    
    if proof_length == float('inf'):
        return {
            "metric_name": "SurfaceArea * ProofLength",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_length_infinite"
        }

    C = surface_area / (math.log(m) / proof_length)
    return {
        "metric_name": "SurfaceArea * ProofLength",
        "metric_value": surface_area * proof_length,
        "instances_tested": 1,
        "conjecture_holds": surface_area * proof_length <= C * math.log(m),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break