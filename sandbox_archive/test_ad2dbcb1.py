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
        for _ in range(int(clause_density * n * (n - 1) / 2)):
            literals = set()
            while len(literals) < 3:
                var = random.randint(1, n)
                polarity = random.choice([True, False])
                literals.add((var, polarity))
            clause = tuple(sorted(literals))
            clauses.append(clause)
        return clauses

    def dpll(clauses):
        assignment = {}
        stack = []
        def unit_propagate():
            while True:
                found_unit_clause = False
                for i, clause in enumerate(clauses):
                    if len(clause) == 1:
                        literal = clause[0]
                        var, polarity = literal
                        if var not in assignment:
                            assignment[var] = polarity
                            stack.append((var, polarity))
                            found_unit_clause = True
                        elif assignment[var] != polarity:
                            return False
                if not found_unit_clause:
                    break
            return True

        def backtracking():
            while stack:
                var, polarity = stack.pop()
                del assignment[var]
                for i in range(len(clauses)):
                    if (var, polarity) in clauses[i]:
                        clauses[i].remove((var, polarity))
                        if not unit_propagate():
                            break
                else:
                    return True
            return False

        if not unit_propagate():
            return None
        if backtracking():
            return assignment
        return None

    def toric_polytope_facets(clauses):
        n = max(var for var, _ in clauses)
        facets = set()
        for clause in clauses:
            facet = tuple(sorted([var for var, _ in clause]))
            facets.add(facet)
        return len(facets)

    def resolution_width(assignment):
        width = 0
        while assignment is not None:
            new_assignment = {}
            for var, polarity in assignment.items():
                if polarity:
                    new_assignment[var] = True
                else:
                    new_assignment[-var] = False
            assignment = dpll(clauses)
            width += 1
        return width

    n = random.randint(5, 40)
    clause_density = random.uniform(0.25, 2.5)
    clauses = generate_3cnf(n, clause_density)
    
    facets = toric_polytope_facets(clauses)
    assignment = dpll(clauses)
    width = resolution_width(assignment) if assignment else None
    
    if width is None:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL failed to find a satisfying assignment"
        }
    
    metric_value = facets / math.log(n)
    conjecture_holds = abs(metric_value - width) < 1e-6
    counterexample = "" if conjecture_holds else f"Facets={facets}, Width={width}"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"resolution_width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")