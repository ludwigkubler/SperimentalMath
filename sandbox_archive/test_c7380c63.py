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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 4):  # Generate a small CNF to avoid trivial cases
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        def simplify(cnf):
            new_cnf = []
            for clause in cnf:
                if not clause:
                    return None
                new_clause = [x for x in clause if x != -x]
                if len(new_clause) == 0:
                    return None
                if len(new_clause) == 1:
                    return new_clause
                new_cnf.append(new_clause)
            return new_cnf

        def unit_propagate(cnf):
            while True:
                unit_clauses = [c[0] for c in cnf if len(c) == 1]
                if not unit_clauses:
                    break
                for u in unit_clauses:
                    cnf = [[x for x in c if x != u and x != -u] for c in cnf if u not in c and -u not in c]
            return cnf

        def pure_literal_propagate(cnf):
            while True:
                purities = {}
                for clause in cnf:
                    for literal in clause:
                        if literal in purities:
                            purities[literal] += 1
                        else:
                            purities[literal] = -1
                unit_clauses = [l for l, count in purities.items() if count == len(cnf)]
                if not unit_clauses:
                    break
                for u in unit_clauses:
                    cnf = [[x for x in c if x != u and x != -u] for c in cnf if u not in c and -u not in c]
            return cnf

        def backtracking(cnf):
            if not cnf:
                return True
            if any(len(c) == 0 for c in cnf):
                return False
            unit_clauses = [c[0] for c in cnf if len(c) == 1]
            if unit_clauses:
                literal = random.choice(unit_clauses)
                new_cnf = [[x for x in c if x != literal and x != -literal] for c in cnf if literal not in c and -literal not in c]
                return backtracking(new_cnf) or backtracking([[x for x in c if x != literal and x != -literal] for c in cnf if literal in c])
            literals = set()
            for clause in cnf:
                literals.update(clause)
            literal = random.choice(list(literals))
            new_cnf_true = [[x for x in c if x != literal and x != -literal] for c in cnf if literal not in c]
            new_cnf_false = [[x for x in c if x != literal and x != -literal] for c in cnf if -literal not in c]
            return backtracking(new_cnf_true) or backtracking(new_cnf_false)

        cnf = simplify(cnf)
        cnf = unit_propagate(cnf)
        cnf = pure_literal_propagate(cnf)
        return backtracking(cnf)

    def free_lie_algebra_rank(cnf):
        n = len(cnf[0])
        generators = list(range(1, n + 1))
        relations = []
        for clause in cnf:
            for i in range(n):
                for j in range(i + 1, n):
                    if (i + 1) * (j + 1) in clause and -(i + 1) * (j + 1) not in clause:
                        relations.append((generators[i], generators[j]))
        rank = len(generators)
        for relation in relations:
            found = False
            for i in range(rank):
                if relation[0] == generators[i]:
                    generators[i] = relation[1]
                    found = True
                    break
            if not found:
                generators.append(relation[1])
                rank += 1
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        w_phi = dpll(cnf)
        if w_phi is None:
            continue
        r_phi = free_lie_algebra_rank(cnf)
        results.append({"n": n, "r_phi": r_phi, "w_phi": w_phi})
    
    if not results:
        return {
            "metric_name": "r_phi / w_phi",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    r_phi_values = [result["r_phi"] for result in results]
    w_phi_values = [result["w_phi"] for result in results]
    mean_r_phi = sum(r_phi_values) / len(r_phi_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    std_r_phi = math.sqrt(sum((x - mean_r_phi)**2 for x in r_phi_values) / len(r_phi_values))
    std_w_phi = math.sqrt(sum((x - mean_w_phi)**2 for x in w_phi_values) / len(w_phi_values))
    
    ratio_values = [r_phi / w_phi for r_phi, w_phi in zip(r_phi_values, w_phi_values)]
    mean_ratio = sum(ratio_values) / len(ratio_values)
    std_ratio = math.sqrt(sum((x - mean_ratio)**2 for x in ratio_values) / len(ratio_values))
    
    if all(0.97 <= r_phi / w_phi <= 1.03 for r_phi, w_phi in zip(r_phi_values, w_phi_values)):
        return {
            "metric_name": "r_phi / w_phi",
            "metric_value": mean_ratio,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "r_phi / w_phi",
            "metric_value": mean_ratio,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": f"Ratio out of bounds: {min(ratio_values)} < r/w < {max(ratio_values)}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed + 1}")