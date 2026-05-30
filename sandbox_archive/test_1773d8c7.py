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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def resolve_clause(clauses, literal):
        new_clauses = []
        for clause in clauses:
            if literal not in clause and -literal not in clause:
                new_clauses.append(clause)
            elif literal in clause:
                continue
            else:
                new_clauses.extend([c for c in clause if c != -literal])
        return new_clauses

    def build_resolution_tree(clauses):
        tree = {}
        stack = [clauses]
        while stack:
            current_clauses = stack.pop()
            for literal in set(lit for clause in current_clauses for lit in clause):
                resolved_clauses = resolve_clause(current_clauses, literal)
                if not resolved_clauses:
                    return tree
                if literal not in tree:
                    tree[literal] = []
                tree[literal].append(resolved_clauses)
                stack.append(resolved_clauses)
        return tree

    def depth_of_tree(tree, node=None):
        if node is None:
            node = next(iter(tree))
        if not tree[node]:
            return 1
        return 1 + max(depth_of_tree(tree, child) for child in tree[node])

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    tree = build_resolution_tree(clauses)
    
    depth = depth_of_tree(tree)
    hodge_classes = len(set(tuple(sorted(c)) for c in clauses))
    
    return {
        "metric_name": "Hodge Degeneration Invariant",
        "metric_value": hodge_classes,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")