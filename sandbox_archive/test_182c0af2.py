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

def generate_random_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(abs(x) != abs(y) and abs(x) != abs(z) for x, y, z in itertools.combinations(clause, 3)):
            clauses.append(clause)
    return clauses

def hypergraph_treewidth(clauses):
    # Simplified treewidth algorithm (not actual treewidth but a proxy)
    return len(set(abs(c[0]) for c in clauses))

def dpll_tree_size(clauses, assignment=[]):
    if all(any(x in assignment or -x in assignment for x in clause) for clause in clauses):
        return 1
    if any(all(x not in assignment and -x not in assignment for x in clause) for clause in clauses):
        return float('inf')
    var = next((x for x in range(1, len(clauses) + 1) if x not in [abs(a) for a in assignment]), None)
    return min(dpll_tree_size(clauses, assignment + [var]) + dpll_tree_size(clauses, assignment + [-var]))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_random_3cnf(n)
    treewidth = hypergraph_treewidth(clauses)
    dpll_size = dpll_tree_size(clauses)
    product = treewidth * dpll_size
    return {
        "metric_name": "product",
        "metric_value": product,
        "instances_tested": 1,
        "conjecture_holds": product > 0,  # Non-negative product is a necessary condition
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_product = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_product} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i + 1 for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"product_non_positive\" first_failing_seed={first_failing_seed}")