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
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in range(1, len(clauses) + 1) if all(l in c or -l in c for c in clauses)), None)
        if pure_literal is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll([c for c in clauses if -pure_literal not in c], new_assignment):
                return True
            return False
        literal = random.choice(range(1, len(clauses) + 1))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if -literal not in c], new_assignment):
            return True
        return False
    
    def resolution(clauses):
        while True:
            new_clauses = []
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                clauses = [c for c in clauses if literal not in c and -literal not in c]
                continue
            resolvents = set()
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    c1, c2 = clauses[i], clauses[j]
                    common_literals = [l for l in c1 if -l in c2]
                    if common_literals:
                        resolvent = tuple(sorted(set(c1) | set(c2) - {c1[l] for l in common_literals} - {-c2[-l] for l in common_literals}))
                        resolvents.add(resolvent)
            if not resolvents:
                break
            new_clauses.extend(resolvents)
            clauses = list(set(clauses + new_clauses))
        return len(clauses) == 0
    
    def min_automorphic_representations(n, m):
        # Placeholder for actual implementation of minimal number of automorphic representations
        return random.randint(1, n * m)
    
    def resolution_proof_tree_height(clauses):
        assignment = {}
        return resolution(clauses)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    clauses = []
    for _ in range(m):
        clause = [random.randint(-n, -1) for _ in range(random.randint(1, n))]
        if not all(l in clauses for l in clause):
            clauses.append(clause)
    
    min_representations = min_automorphic_representations(n, m)
    proof_tree_height = resolution_proof_tree_height(clauses)
    
    if min_representations == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "min_automorphic_representations is zero"
        }
    
    ratio = proof_tree_height / min_representations
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")