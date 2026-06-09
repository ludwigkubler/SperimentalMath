# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
        pure_literals = [l for l in range(1, max(assignment.keys()) + 1) if all(l not in c or -l not in c for c in clauses)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
        for literal in range(1, max(assignment.keys()) + 2):
            if literal not in assignment:
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
                new_assignment[literal] = False
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
        return False
    
    def cnf_to_tiling(cnf):
        n = len(cnf)
        tiling = [[0] * (2 * n) for _ in range(2 * n)]
        for i, clause in enumerate(cnf):
            for literal in clause:
                row = (i + literal) % (2 * n)
                col = abs(literal) - 1
                tiling[row][col] = 1
        return tiling
    
    def find_automorphisms(tiling):
        n = len(tiling)
        automorphisms = []
        for perm in permutations(range(n)):
            if all(tiling[perm[i]][j] == tiling[i][perm[j]] for i in range(n) for j in range(n)):
                automorphisms.append(perm)
        return automorphisms
    
    def min_order(G):
        return len(G)
    
    def frege_proof_depth(cnf):
        assignment = {}
        if dpll(cnf, assignment):
            return 0
        stack = [(cnf, assignment)]
        depth = 0
        while stack:
            clauses, assignment = stack.pop()
            unit_clauses = [c for c in clauses if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0][0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                stack.append((clauses, new_assignment))
                new_assignment[literal] = False
                stack.append((clauses, new_assignment))
            else:
                pure_literals = [l for l in range(1, max(assignment.keys()) + 1) if all(l not in c or -l not in c for c in clauses)]
                if pure_literals:
                    literal = pure_literals[0]
                    new_assignment = assignment.copy()
                    new_assignment[literal] = True
                    stack.append((clauses, new_assignment))
                    new_assignment[literal] = False
                    stack.append((clauses, new_assignment))
                else:
                    for literal in range(1, max(assignment.keys()) + 2):
                        if literal not in assignment:
                            new_assignment = assignment.copy()
                            new_assignment[literal] = True
                            stack.append((clauses, new_assignment))
                            new_assignment[literal] = False
                            stack.append((clauses, new_assignment))
            depth += 1
        return depth
    
    n_max = 40
    instances_tested = 0
    total_metric_value = Fraction(0)
    
    for n in range(5, 41):
        cnf = [random.choice([[-i], [i]]) for i in range(1, n + 1)]
        tiling = cnf_to_tiling(cnf)
        G = find_automorphisms(tiling)
        d_phi = frege_proof_depth(cnf)
        
        instances_tested += 1
        total_metric_value += Fraction(math.log(min_order(G)), d_phi)
    
    if instances_tested < 30:
        return {
            "metric_name": "log_min_order_over_d_phi",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = Fraction(0)
    for i in range(instances_tested):
        std_metric_value += (total_metric_value - mean_metric_value) ** 2
    std_metric_value /= instances_tested
    std_metric_value = math.sqrt(std_metric_value)
    
    return {
        "metric_name": "log_min_order_over_d_phi",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_metric_value >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")