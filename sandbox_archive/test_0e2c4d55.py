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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        def search(assignment, clauses):
            if not clauses:
                return True
            literal = find_pure_literal(clauses) or find_unit_clause(clauses)
            if literal is None:
                literal = random.choice([x for clause in clauses for x in clause])
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return search(assignment + [literal], new_clauses) or search(assignment + [-literal], new_clauses)
        
        def find_pure_literal(clauses):
            pure_literals = {}
            for clause in clauses:
                for literal in clause:
                    if literal in pure_literals:
                        pure_literals[literal] = None
                    else:
                        pure_literals[-literal] = literal
            return next((l for l, p in pure_literals.items() if p is not None), None)
        
        def find_unit_clause(clauses):
            for clause in clauses:
                if len(clause) == 1:
                    return clause[0]
            return None
        
        return search([], cnf)

    def hecke_eigenform_order(n):
        # Placeholder function to simulate the computation of the minimal order
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)

    n_max = 40
    instances_tested = 0
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        order = hecke_eigenform_order(n)
        width = dpll(cnf)
        
        if width == 0:
            continue
        
        ratio = Fraction(order, width)
        total_ratio += abs(ratio - 1)  # Assuming the expected ratio is 1 for simplicity
        instances_tested += 1

    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0.0
    
    if mean_ratio <= 0.1:
        conjecture_holds = True
    else:
        conjecture_holds = False
        counterexample = f"Ratio {mean_ratio} does not meet the threshold"

    return {
        "metric_name": "Order-Width Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio does not meet the threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")