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

def generate_random_kcnf(n, k):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(k):
        clause = set()
        while len(clause) < 3:
            literal = random.choice(variables)
            if -literal not in clause:
                clause.add(literal)
        clauses.append(tuple(sorted(clause)))
    return variables, clauses

def dpll(variables, assignment):
    unsatisfied_clauses = [c for c in clauses if any(v in assignment and assignment[v] == True or -v in assignment and assignment[v] == False for v in c)]
    if not unsatisfied_clauses:
        return 0
    pure_literal = next((v for v in variables if all(v not in c or -v not in c for c in unsatisfied_clauses)), None)
    if pure_literal is None:
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause is None:
            return float('inf')
        literal, = unit_clause
    else:
        literal = pure_literal
    new_assignment = assignment.copy()
    new_assignment[literal] = True
    depth_true = dpll(variables, new_assignment) + 1
    new_assignment[literal] = False
    depth_false = dpll(variables, new_assignment) + 1
    return min(depth_true, depth_false)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_random_kcnf(n, k=3*n)
        depth = dpll(variables, {})
        expected_depth = Fraction(1, 1) * n * math.log(n)
        results.append({
            "n": n,
            "depth": depth,
            "expected_depth": expected_depth
        })
    
    total_depth = sum(r["depth"] for r in results)
    mean_depth = total_depth / len(results)
    std_dev = math.sqrt(sum((r["depth"] - mean_depth) ** 2 for r in results) / len(results))
    
    correlation_bound = 0.5
    if any(abs(r["depth"] - r["expected_depth"]) > 3 * std_dev for r in results):
        conjecture_holds = False
        counterexample = "Depth exceeds expected by more than 3 standard deviations"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "DPLL Tree Depth",
        "metric_value": mean_depth,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_depth = sum(r["metric_value"] for r in results)
    mean_depth = total_depth / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Depth exceeds expected by more than 3 std deviations' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")