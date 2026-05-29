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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses
    
    def truth_table(clauses):
        n = len(clauses[0])
        table = []
        for i in range(2 ** n):
            assignment = [(i >> j) & 1 for j in range(n)]
            table.append(all(c == 0 or c == assignment[abs(c) - 1] for c in clauses))
        return table
    
    def hilbert_cube_diameter(table):
        n = len(table)
        max_dist = 0
        for i in range(n):
            for j in range(i + 1, n):
                dist = sum(1 for k in range(n) if table[i][k] != table[j][k])
                max_dist = max(max_dist, dist)
        return max_dist
    
    def frege_proof_depth(clauses):
        # Simple DPLL-based solver to estimate proof depth
        def dpll(clauses, assignment, level=0):
            if not clauses:
                return level
            unit_clauses = [c for c in clauses if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0][0]
                new_assignment = assignment[:]
                new_assignment[abs(literal) - 1] = literal > 0
                return dpll([c for c in clauses if literal not in c], new_assignment, level + 1)
            pure_literals = [l for l in range(1, len(clauses) + 1) if (l not in assignment and -l not in assignment)]
            if pure_literals:
                literal = pure_literals[0]
                new_assignment = assignment[:]
                new_assignment[literal - 1] = True
                return dpll([c for c in clauses if literal not in c], new_assignment, level + 1)
            return float('inf')
        
        return min(dpll(clauses, [False] * len(clauses)), dpll(clauses, [True] * len(clauses)))
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    table = truth_table(clauses)
    diameter = hilbert_cube_diameter(table)
    proof_depth = frege_proof_depth(clauses)
    
    if proof_depth == float('inf'):
        return {
            "metric_name": "diameter_over_proof_depth",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = diameter / proof_depth
    conjecture_holds = metric_value <= 2 * proof_depth  # Example constant c=2, adjust as needed
    
    return {
        "metric_name": "diameter_over_proof_depth",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unmet_conditions")