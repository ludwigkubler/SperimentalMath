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
    
    def generate_formula(n):
        clauses = []
        for i in range(2**n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
            if not any(clause[j] == -clause[j-1] for j in range(1, n)):
                clauses.append(clause)
        return clauses

    def dpll_width(clauses):
        def dpll(clauses, assignment):
            if not clauses:
                return 0
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                return dpll(new_clauses, new_assignment) + 1
            pure_literal = next((l for l in range(1, n+1) if (all(l in c or -l in c for c in clauses)) and (-l in assignment)), None)
            if pure_literal:
                new_assignment[pure_literal] = True
                new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
                return dpll(new_clauses, new_assignment) + 1
            literal = random.choice([l for l in range(1, n+1)])
            new_assignment[literal] = True
            new_clauses_true = [c for c in clauses if literal not in c and -literal not in c]
            new_clauses_false = [c for c in clauses if -literal not in c and literal not in c]
            return max(dpll(new_clauses_true, new_assignment), dpll(new_clauses_false, new_assignment)) + 1
        n = len(clauses[0])
        assignment = {}
        return dpll(clauses, assignment)

    def symmetric_group_order(n):
        if n == 0:
            return 1
        order = 1
        for i in range(1, n+1):
            order *= i
        return order

    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    w_DPLL = dpll_width(formula)
    G_order = symmetric_group_order(n)

    return {
        "metric_name": "Spearman's rank correlation",
        "metric_value": None,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] >= 0.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='Spearman correlation below 0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")