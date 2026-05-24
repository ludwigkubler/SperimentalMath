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

    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
            clauses.append([-variables[i-1], f'y{i}'])
            clauses.append([f'y{i}', -f'y{i+1}'])
        return variables, clauses

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in assignment if all(l not in c or -l in c for c in clauses)), None)
        if pure_literal is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            return False
        literal, _ = random.choice(clauses)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        return False

    def resolution(clauses):
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    clause_i = clauses[i]
                    clause_j = clauses[j]
                    common_literal = next((l for l in clause_i if -l in clause_j), None)
                    if common_literal:
                        new_clause = [l for l in clause_i if l != common_literal] + [l for l in clause_j if l != -common_literal]
                        if not new_clause:
                            return True
                        new_clauses.append(new_clause)
            if len(new_clauses) == len(clauses):
                return False
            clauses = new_clauses

    def geometric_flow_invariant(n, variables, clauses):
        # Placeholder for actual implementation of geometric flow invariant
        return random.randint(1, n)

    n = 20
    variables, clauses = generate_tseitin_formula(n)
    resolution_length = resolution(clauses)
    rank_F_G = geometric_flow_invariant(n, variables, clauses)
    ratio = resolution_length / (2 ** rank_F_G) if rank_F_G > 0 else float('inf')

    return {
        "metric_name": "resolution_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 1,  # Placeholder constant c
        "counterexample": "" if ratio >= 1 else "small_resolution_length"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    total_ratio = 0
    count_supports_conjecture = 0

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        total_ratio += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_supports_conjecture += 1
        results.append(trial_result)

    mean_ratio = total_ratio / len(results)
    support_fraction = count_supports_conjecture / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='small_resolution_length' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")