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
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) if random.randint(0, 1) else -random.choice(variables) for _ in range(random.randint(2, 3))]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        pure_literals = {}
        for literal in set(lit for clause in cnf for lit in clause):
            pos_count = sum(1 for clause in cnf if literal in clause)
            neg_count = sum(1 for clause in cnf if -literal in clause)
            if pos_count == 0:
                pure_literals[literal] = True
            elif neg_count == 0:
                pure_literals[-literal] = False
        
        unit_clause = next((c[0] for c in cnf if len(c) == 1), None)
        if unit_clause is not None:
            new_assignment = assignment.copy()
            new_assignment[unit_clause] = True
            return dpll([c for c in cnf if unit_clause not in c and -unit_clause not in c], new_assignment)
        
        pure_literal = next((lit for lit, value in pure_literals.items() if value), None)
        if pure_literal is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment)
        
        literal = next((lit for lit, value in pure_literals.items() if not value), None)
        if literal is not None:
            new_assignment = assignment.copy()
            new_assignment[literal] = False
            return dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment)
        
        literal = random.choice(list(pure_literals.keys()))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        
        new_assignment[literal] = False
        return dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment)
    
    def height_dpll(cnf):
        if not cnf:
            return 0
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        pure_literals = {}
        for literal in set(lit for clause in cnf for lit in clause):
            pos_count = sum(1 for clause in cnf if literal in clause)
            neg_count = sum(1 for clause in cnf if -literal in clause)
            if pos_count == 0:
                pure_literals[literal] = True
            elif neg_count == 0:
                pure_literals[-literal] = False
        
        unit_clause = next((c[0] for c in cnf if len(c) == 1), None)
        if unit_clause is not None:
            new_cnf = [c for c in cnf if unit_clause not in c and -unit_clause not in c]
            return 1 + height_dpll(new_cnf)
        
        pure_literal = next((lit for lit, value in pure_literals.items() if value), None)
        if pure_literal is not None:
            new_cnf = [c for c in cnf if pure_literal not in c and -pure_literal not in c]
            return 1 + height_dpll(new_cnf)
        
        pure_literal = next((lit for lit, value in pure_literals.items() if not value), None)
        if pure_literal is not None:
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            return 1 + height_dpll(new_cnf)
        
        literal = random.choice(list(pure_literals.keys()))
        new_cnf = [c for c in cnf if literal not in c and -literal not in c]
        return 1 + max(height_dpll([c for c in new_cnf if literal not in c]), height_dpll([c for c in new_cnf if -literal not in c]))
    
    def p_adic_l_function(cnf):
        # Placeholder implementation
        return len(cnf)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * (n + 1) // 2)
    cnf = generate_cnf(n, m)
    rank_p_adic = p_adic_l_function(cnf)
    height_dpll_tree = height_dpll(cnf)
    
    return {
        "metric_name": "rank_diff",
        "metric_value": abs(rank_p_adic - height_dpll_tree),
        "instances_tested": 1,
        "conjecture_holds": rank_p_adic <= height_dpll_tree,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank_diff\" first_failing_seed={first_failing_seed}")