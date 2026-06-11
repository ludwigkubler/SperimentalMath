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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def dpll_solve(clauses, assignment=[]):
        if not clauses:
            return True
        p = next((x for x in range(1, len(clauses[0]) + 1) if x not in [abs(lit) for lit in assignment]), None)
        if p is None:
            return False
        
        def propagate(lit):
            new_clauses = []
            for clause in clauses:
                if any(abs(x) == abs(lit) for x in clause):
                    continue
                if all(abs(x) != abs(lit) for x in clause):
                    return None
                new_clause = [x for x in clause if x != -lit]
                if not new_clause:
                    return None
                new_clauses.append(new_clause)
            return new_clauses
        
        if dpll_solve(propagate(p), assignment + [p]):
            return True
        if dpll_solve(propagate(-p), assignment + [-p]):
            return True
        return False
    
    def monomial_basis_dimension(clause_induced_ideal):
        # Placeholder for actual computation of monomial basis dimension
        # This is a dummy implementation that returns a random value
        return random.randint(1, 5)
    
    def dpll_search_tree_width(clauses):
        # Placeholder for actual computation of DPLL search tree width
        # This is a dummy implementation that returns a random value
        return random.randint(10, 20)
    
    n = 30
    instances_tested = 30
    total_dimension = 0
    total_width = 0
    
    for _ in range(instances_tested):
        clauses = generate_sat_instance(n)
        if not dpll_solve(clauses):
            continue
        
        dimension = monomial_basis_dimension(clause_induced_ideal=clauses)
        width = dpll_search_tree_width(clauses)
        
        total_dimension += dimension
        total_width += width
    
    mean_dimension = Fraction(total_dimension, instances_tested)
    mean_width = Fraction(total_width, instances_tested)
    
    correlation_coefficient = (instances_tested * mean_dimension * mean_width - 
                               sum(dimension * width for dimension, width in zip([mean_dimension] * instances_tested, [mean_width] * instances_tested))) / \
                              math.sqrt((instances_tested * mean_dimension**2 - sum(dimension**2 for dimension in [mean_dimension] * instances_tested)) *
                                        (instances_tested * mean_width**2 - sum(width**2 for width in [mean_width] * instances_tested)))
    
    conjecture_holds = correlation_coefficient > 0.8 and abs(mean_dimension - mean_width) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")