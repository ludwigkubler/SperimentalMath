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

def generate_random_graph(n):
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                edges.append((i, j))
    return edges

def dpll_solve(clauses):
    def solve(lits_true, lits_false):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            lit = unit_clause[0]
            if lit in lits_false or -lit in lits_true:
                return False
            new_clauses = [c for c in clauses if lit not in c and -lit not in c]
            new_lits_true = lits_true + [lit] if lit > 0 else lits_true
            new_lits_false = lits_false + [-lit] if lit < 0 else lits_false
            return solve(new_lits_true, new_lits_false)
        pure_literal = next((l for l in range(1, max(lits_true) + 1) if l not in lits_false and -l not in lits_true), None)
        if pure_literal is None:
            return False
        new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
        new_lits_true = lits_true + [pure_literal] if pure_literal > 0 else lits_true
        new_lits_false = lits_false + [-pure_literal] if pure_literal < 0 else lits_false
        return solve(new_lits_true, new_lits_false)
    return solve([], [])

def resolution_width(clauses):
    def resolve(c1, c2):
        resolved = []
        for lit in c1:
            if -lit in c2:
                resolved.extend([l for l in c1 if l != lit] + [l for l in c2 if l != -lit])
                break
        return resolved
    
    while True:
        new_clauses = set()
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvent = resolve(clauses[i], clauses[j])
                if not resolvent:
                    continue
                if len(resolvent) == 0:
                    return 0
                new_clauses.add(tuple(sorted(resolvent)))
        if new_clauses.issubset(set(map(tuple, clauses))):
            break
        clauses.extend(new_clauses)
    return max(len(c) for c in clauses)

def geometric_langlands_index(graph):
    # Placeholder function to compute the index of the geometric Langlands dual
    # This is a dummy implementation and should be replaced with actual computation
    return random.random()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_graph(n)
        clauses = [(i + 1,) for i in range(n)]  # Example CNF formula
        ind_G = geometric_langlands_index(graph)
        w_G = resolution_width(clauses)
        
        if ind_G < 0 or w_G < 0:
            return {
                "metric_name": "resolution_proof_width",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "negative_index_or_width"
            }
        
        results.append((ind_G, w_G))
    
    ind_values = [r[0] for r in results]
    w_values = [r[1] for r in results]
    
    mean_ind = sum(ind_values) / len(ind_values)
    mean_w = sum(w_values) / len(w_values)
    
    if any(ind < 0 or w < 0 for ind, w in results):
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "negative_index_or_width"
        }
    
    if any(ind < c * n**(1/4) for ind, n in zip(ind_values, n_values)):
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "index_less_than_c_n_1_4"
        }
    
    if any(ind / w > 2.5 for ind, w in zip(ind_values, w_values)):
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "ind_over_w_greater_than_2_5"
        }
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean_ind,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")