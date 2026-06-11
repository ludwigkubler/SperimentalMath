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
    
    def generate_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * i for i in range(1, n+1)]
            clauses.append(clause)
        return clauses
    
    def construct_mapping(clauses):
        groups = {}
        for literal in set(lit for clause in clauses for lit in clause):
            if literal not in groups:
                groups[literal] = []
            for clause in clauses:
                if literal in clause:
                    groups[literal].append(clause)
        return groups
    
    def measure_resolution_width(clauses):
        # Simplified DPLL solver to estimate width
        stack = []
        assignment = {}
        for literal in set(lit for clause in clauses for lit in clause):
            assignment[literal] = None
        
        def dpll():
            if not clauses:
                return 1
            var, polarity = find_pure_literal(clauses)
            if var is None:
                return max(dpll(), dpll())
            assignment[var] = polarity
            new_clauses = [c for c in clauses if not evaluate_clause(c)]
            if evaluate_clause([var]):
                return dpll()
            assignment[var] = -polarity
            if evaluate_clause([-var]):
                return dpll()
            assignment[var] = None
            return 0
        
        def find_pure_literal(clauses):
            pure_literals = {}
            for literal in set(lit for clause in clauses for lit in clause):
                polarity_count = sum(1 for c in clauses if literal in c) - sum(1 for c in clauses if -literal in c)
                if polarity_count == len(clauses):
                    return literal, 1
                elif polarity_count == -len(clauses):
                    return literal, -1
            return None, None
        
        def evaluate_clause(clause):
            for lit in clause:
                if assignment[lit] is not None and assignment[lit] != lit // abs(lit):
                    return False
            return True
        
        width = dpll()
        return width
    
    def order_crossed_product(groups):
        # Simplified calculation of crossed product order
        order = 1
        for group in groups.values():
            order *= len(group)
        return order
    
    n = random.randint(5, 40)
    instance = generate_instance(n)
    mapping = construct_mapping(instance)
    width = measure_resolution_width(instance)
    order = order_crossed_product(mapping)
    
    return {
        "metric_name": "OrderCrossedProduct",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if order == width else False,
        "counterexample": "" if order == width else f"Order={order}, Width={width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 1.0 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["metric_value"] > 1.0)
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient > 1.0' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")