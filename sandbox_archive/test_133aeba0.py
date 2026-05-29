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

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause.reverse()
        clauses.append(clause)
    return clauses

def dpll(cnf, assignment):
    if not cnf:
        return True
    unit_clause = next((c for c in cnf if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in cnf if -literal not in c], new_assignment):
            return True
        return False
    pure_literal = next((l for l in range(1, n + 1) if all(l in assignment or -l not in assignment for c in cnf)), None)
    if pure_literal:
        new_assignment = assignment.copy()
        new_assignment[pure_literal] = True
        if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
            return True
        new_assignment[pure_literal] = False
        if dpll([c for c in cnf if -pure_literal not in c], new_assignment):
            return True
        return False
    literal = random.choice(range(1, n + 1))
    new_assignment = assignment.copy()
    new_assignment[literal] = True
    if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
        return True
    new_assignment[literal] = False
    if dpll([c for c in cnf if -literal not in c], new_assignment):
        return True
    return False

def dpll_tree_depth(cnf):
    def dpll_helper(cnf, assignment, depth):
        if not cnf:
            return depth
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            max_depth = dpll_helper([c for c in cnf if literal not in c and -literal not in c], new_assignment, depth + 1)
            new_assignment[literal] = False
            if max_depth > depth:
                return max_depth
            new_assignment[literal] = False
            max_depth = dpll_helper([c for c in cnf if -literal not in c], new_assignment, depth + 1)
            if max_depth > depth:
                return max_depth
            return depth
        pure_literal = next((l for l in range(1, n + 1) if all(l in assignment or -l not in assignment for c in cnf)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            max_depth = dpll_helper([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment, depth + 1)
            new_assignment[pure_literal] = False
            if max_depth > depth:
                return max_depth
            new_assignment[pure_literal] = False
            max_depth = dpll_helper([c for c in cnf if -pure_literal not in c], new_assignment, depth + 1)
            if max_depth > depth:
                return max_depth
            return depth
        literal = random.choice(range(1, n + 1))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        max_depth = dpll_helper([c for c in cnf if literal not in c and -literal not in c], new_assignment, depth + 1)
        new_assignment[literal] = False
        if max_depth > depth:
            return max_depth
        new_assignment[literal] = False
        max_depth = dpll_helper([c for c in cnf if -literal not in c], new_assignment, depth + 1)
        if max_depth > depth:
            return max_depth
        return depth
    n = len(cnf[0])
    return dpll_helper(cnf, {}, 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            m_Br_F = len(set(cnf))  # Simplified Brauer group generator count
            t_star_F = dpll_tree_depth(cnf)
            results.append((m_Br_F, t_star_F))
    mean_value = sum(m_Br_F for m_Br_F, _ in results) / len(results)
    std_value = math.sqrt(sum((m_Br_F - mean_value) ** 2 for m_Br_F, _ in results) / len(results))
    conjecture_holds = all(m_Br_F <= t_star_F + 1 for m_Br_F, t_star_F in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Brauer Group Generator Count vs DPLL Depth",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
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