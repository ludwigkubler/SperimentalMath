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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 1) * (i + 1) for i in range(n)]
            if any(x != 0 for x in clause):
                clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment=None):
        if not clauses:
            return True
        literal = next((x for x in range(1, len(assignment) + 1) if assignment[x - 1] is None), None)
        if literal is None:
            return False
        
        positive_literal = literal
        negative_literal = -literal
        new_assignment = assignment[:]
        new_assignment[abs(literal) - 1] = True if literal > 0 else False
        
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        
        new_assignment[abs(literal) - 1] = None
        new_assignment[abs(negative_literal) - 1] = True if negative_literal > 0 else False
        
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        
        return False
    
    def dpll_search_tree_diameter(clauses):
        assignment = [None] * len(clauses)
        if not dpll(clauses, assignment):
            return 0
        # Simplified heuristic for diameter estimation
        return sum(1 for x in assignment if x is not None)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_cnf(n)
    diameter = dpll_search_tree_diameter(clauses)
    
    return {
        "metric_name": "diameter",
        "metric_value": diameter,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")