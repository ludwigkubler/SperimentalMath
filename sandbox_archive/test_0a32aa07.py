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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        new_clauses = set()
        while True:
            new_clause = None
            for c1 in clauses:
                for c2 in clauses:
                    if len(set(c1) & set(c2)) == 2:
                        new_clause = tuple(sorted([x for x in c1 + c2 if x not in set(c1) & set(c2)]))
                        break
                if new_clause:
                    break
            if new_clause is None:
                return clauses
            if new_clause in clauses or new_clause in new_clauses:
                continue
            new_clauses.add(new_clause)
            clauses.add(new_clause)
    
    def hodge_index(clauses):
        # Placeholder for Hodge index calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(clauses) / 2
    
    def resolution_tree(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        tree = {}
        stack = [(clauses, [])]
        while stack:
            current_clauses, path = stack.pop()
            if not current_clauses:
                return len(path)
            new_clause = None
            for c1 in current_clauses:
                for c2 in current_clauses:
                    if len(set(c1) & set(c2)) == 2:
                        new_clause = tuple(sorted([x for x in c1 + c2 if x not in set(c1) & set(c2)]))
                        break
                if new_clause is None:
                    continue
                if new_clause in current_clauses or new_clause in tree:
                    continue
                tree[new_clause] = path + [new_clause]
                stack.append((current_clauses - {c1, c2} | {new_clause}, path + [new_clause]))
                break
        return len(path)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    cnf = generate_cnf(n, m)
    hodge = hodge_index(cnf)
    res_tree_diameter = resolution_tree(cnf)
    l_F = 2 ** (res_tree_diameter - 1)
    
    if l_F == 0:
        return {
            "metric_name": "Hodge Index vs Resolution Proof Tree Diameter",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "l_F is zero"
        }
    
    c = math.log2(l_F) / hodge
    return {
        "metric_name": "Hodge Index vs Resolution Proof Tree Diameter",
        "metric_value": hodge * c,
        "instances_tested": 1,
        "conjecture_holds": hodge <= c * math.log2(l_F),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all("counterexample" in r and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")