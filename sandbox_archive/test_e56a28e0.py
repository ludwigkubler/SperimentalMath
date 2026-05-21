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
    
    def generate_3cnf(n, clause_density):
        clauses = []
        for _ in range(int(n * n * clause_density / 2)):
            literals = [random.randint(1, n), random.randint(1, n)]
            if random.choice([True, False]):
                literals[0] *= -1
            if random.choice([True, False]):
                literals[1] *= -1
            clauses.append(tuple(literals))
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and -literal in assignment:
                return False
            assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return dpll(new_clauses, assignment)
        pure_literal = next((l for l in range(1, n + 1) if (l not in assignment and -l not in [c[0] for c in clauses]) or (-l not in assignment and -l not in [-c[0] for c in clauses])), None)
        if pure_literal:
            assignment[pure_literal] = True
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return dpll(new_clauses, assignment)
        literal = random.choice([l for l in range(1, n + 1) if l not in assignment])
        assignment[literal] = True
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        if dpll(new_clauses, assignment):
            return True
        assignment[literal] = False
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        if dpll(new_clauses, assignment):
            return True
        return False
    
    def resolution_width(clauses):
        queue = list(clauses)
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue:
                common_literals = [l for l in clause1 if -l in clause2]
                if len(common_literals) == 1:
                    new_clause = tuple(l for l in clause1 + clause2 if l not in common_literals and -l not in common_literals)
                    if len(new_clause) == 0:
                        return 1
                    if new_clause not in queue:
                        queue.append(new_clause)
        return float('inf')
    
    def toric_polytope_facets(clauses):
        n = max(abs(l) for c in clauses for l in c)
        facets = set()
        for clause in clauses:
            facet = tuple(sorted([n + i if l > 0 else -n - i for l, i in zip(clause, range(1, len(clause) + 1))]))
            facets.add(facet)
        return len(facets)
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n, 2.5)
    resolution_width_value = resolution_width(clauses)
    facets_count = toric_polytope_facets(clauses)
    
    if resolution_width_value == float('inf'):
        return {
            "metric_name": "resolution_width",
            "metric_value": resolution_width_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Resolution width is infinite for this instance"
        }
    
    metric_value = facets_count / math.log(n)
    conjecture_holds = abs(metric_value - resolution_width_value) < 0.1 * resolution_width_value
    counterexample = "" if conjecture_holds else f"Facets count: {facets_count}, Log n: {math.log(n)}, Resolution width: {resolution_width_value}"
    
    return {
        "metric_name": "facet_count",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples")