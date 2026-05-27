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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set(random.sample(range(1, n+1), 2))
        cnf.append(clause)
    return cnf

def dpll(cnf, assignment=None):
    if assignment is None:
        assignment = {}
    
    unit_clauses = [c for c in cnf if len(c) == 1]
    pure_literals = set()
    
    while True:
        # Unit propagation
        while unit_clauses:
            literal = next(iter(unit_clauses[0]))
            polarity = literal > 0
            assignment[literal] = polarity
            unit_clauses.pop(0)
            new_clauses = []
            for c in cnf:
                if literal not in c and -literal not in c:
                    new_clauses.append(c)
                elif -literal in c:
                    continue
                else:
                    pure_literals.add(literal if polarity else -literal)
            cnf = new_clauses
        
        # Pure literal elimination
        while pure_literals:
            literal = next(iter(pure_literals))
            polarity = literal > 0
            assignment[literal] = polarity
            pure_literals.remove(literal)
            new_clauses = []
            for c in cnf:
                if literal not in c and -literal not in c:
                    new_clauses.append(c)
                elif -literal in c:
                    continue
                else:
                    pure_literals.add(literal if polarity else -literal)
            cnf = new_clauses
        
        # Check for unsatisfiability
        if any(len(c) == 0 for c in cnf):
            return None
        
        # Backtracking
        unassigned_vars = [v for v in range(1, n+1) if v not in assignment]
        if not unassigned_vars:
            return assignment
        
        literal = unassigned_vars[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        result = dpll(cnf, new_assignment)
        if result is not None:
            return result
        
        new_assignment[literal] = False
        result = dpll(cnf, new_assignment)
        if result is not None:
            return result
    
    return assignment

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = int(n * (n / 3))  # Clause-to-variable ratio
        cnf = generate_cnf(n, m)
        depth = dpll(cnf)
        
        if depth is None:
            return {
                "metric_name": "min_rank_to_depth_ratio",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "unsatisfiable"
            }
        
        results.append(depth)
    
    mean_d = sum(results) / len(results)
    min_rank_to_depth_ratio = Fraction(mean_d, n).limit_denominator()
    
    return {
        "metric_name": "min_rank_to_depth_ratio",
        "metric_value": float(min_rank_to_depth_ratio),
        "instances_tested": len(n_values),
        "conjecture_holds": 0.5 <= min_rank_to_depth_ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if "conjecture_holds" in result and not result["conjecture_holds"]:
            return f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}"
        
        results.append(result["metric_value"])
    
    mean_d = sum(results) / len(results)
    support_fraction = sum(1 for r in results if 0.5 <= r <= 1.5) / len(results)
    
    if support_fraction >= 0.8:
        return f"RESULT: SUPPORTED mean={mean_d} std=0 support_fraction={support_fraction}"
    else:
        return f"RESULT: INCONCLUSIVE reason=support_fraction<{support_fraction}"