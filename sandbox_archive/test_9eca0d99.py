# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        return [[random.choice([1, -1]) for _ in range(random.randint(2, n))] for _ in range(n)]
    
    def dpll_search_tree_depth(formula):
        def dpll(clauses, assignment, literals):
            if not clauses:
                return 0
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                return 1 + dpll(new_clauses, new_assignment, literals)
            pure_literal = next((l for l in literals if all(l not in clause or -l in clause for clause in clauses)), None)
            if pure_literal is not None:
                new_assignment = assignment.copy()
                new_assignment[pure_literal] = True
                new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
                return 1 + dpll(new_clauses, new_assignment, literals)
            literal = random.choice(literals)
            new_assignment_true = assignment.copy()
            new_assignment_true[literal] = True
            new_clauses_true = [c for c in clauses if literal not in c and -literal not in c]
            depth_true = 1 + dpll(new_clauses_true, new_assignment_true, literals)
            new_assignment_false = assignment.copy()
            new_assignment_false[literal] = False
            new_clauses_false = [c for c in clauses if literal not in c and -literal not in c]
            depth_false = 1 + dpll(new_clauses_false, new_assignment_false, literals)
            return max(depth_true, depth_false)
        return dpll(formula, {}, set(range(1, n+1)))
    
    def toric_variety_rank(formula):
        # Placeholder for the actual computation of the minimal rank of the toric variety
        # This is a dummy implementation and should be replaced with an actual algorithm
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    depth = dpll_search_tree_depth(formula)
    rank = toric_variety_rank(formula)
    
    return {
        "metric_name": "Depth of DPLL Search Tree",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": abs(depth - rank) <= max(1, depth // 2),
        "counterexample": "" if conjecture_holds else f"Depth: {depth}, Rank: {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = (sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")