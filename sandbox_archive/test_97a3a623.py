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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[-abs(literal)] = literal > 0
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                del new_assignment[-abs(literal)]
        pure_literal = next((l for l in range(1, n + 1) if all(l not in c or -l not in c for c in cnf)), None)
        if pure_literal is not None:
            new_assignment[pure_literal] = True
            if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            else:
                del new_assignment[pure_literal]
        literal = random.choice(range(1, n + 1))
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        else:
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False
    
    def resolution(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        while True:
            new_clauses = []
            for c1, c2 in itertools.combinations(clauses, 2):
                if len(set(c1) & set(c2)) == 1:
                    literal = next(l for l in set(c1) if l not in set(c2))
                    new_clause = tuple(sorted([l for l in c1 + c2 if l != -literal]))
                    if new_clause not in clauses:
                        new_clauses.append(new_clause)
            if not new_clauses:
                return len(clauses)
            clauses.update(new_clauses)
    
    def free_lie_algebra_rank(cnf):
        n = max(abs(l) for clause in cnf for l in clause)
        generators = list(range(1, n + 1))
        relations = []
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    relations.append((clause[i], clause[j]))
        rank = 0
        while relations:
            relation = relations.pop(0)
            if relation[0] != -relation[1]:
                rank += 1
                new_relations = []
                for r in relations:
                    if r[0] == relation[0] or r[1] == relation[0]:
                        new_relations.append((r[0], -relation[1]))
                    elif r[0] == relation[1] or r[1] == relation[1]:
                        new_relations.append((-relation[0], r[1]))
                relations = new_relations
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            w_phi = resolution(cnf)
            r_phi = free_lie_algebra_rank(cnf)
            if w_phi == 0 or r_phi == 0:
                continue
            results.append((n, w_phi, r_phi))
    
    if not results:
        return {
            "metric_name": "r_phi_over_w_phi",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _, _ in results)
    instances_tested = len(results)
    r_phi_over_w_phi_values = [r_phi / w_phi for _, w_phi, r_phi in results]
    mean_r_phi_over_w_phi = sum(r_phi_over_w_phi_values) / instances_tested
    std_r_phi_over_w_phi = math.sqrt(sum((x - mean_r_phi_over_w_phi) ** 2 for x in r_phi_over_w_phi_values) / instances_tested)
    
    return {
        "metric_name": "r_phi_over_w_phi",
        "metric_value": mean_r_phi_over_w_phi,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(0.97 <= x / y <= 1.03 for _, y, x in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    results = [run_trial(seed)["metric_value"] for seed in seeds if run_trial(seed)["metric_value"] is not None]
    support_fraction = sum(1 for r in results if 0.97 <= r / max(results) <= 1.03) / len(results)
    
    if all(r is not None for r in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
        print(f"{RESULT} mean={sum(results)/len(results):.2f} std={math.sqrt(sum((x - sum(results)/len(results))**2 for x in results) / len(results)):.2f} support_fraction={support_fraction:.2f}")
    elif any(r is None for r in results):
        RESULT = "INCONCLUSIVE" if all(r is not None for r in results) else "FALSIFIED"
        print(f"{RESULT} counterexample=\"mapping_undefined\" first_failing_seed=1")