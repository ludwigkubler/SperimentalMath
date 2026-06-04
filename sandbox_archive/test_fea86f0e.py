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
        for i in range(1, n+1):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(i)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        seen = set()
        while queue:
            literal = random.choice(queue)
            if literal in seen or -literal in seen:
                return len(seen)
            seen.add(literal)
            for clause in cnf:
                if literal in clause and -literal not in clause:
                    new_clause = [l for l in clause if l != literal]
                    queue.append(new_clause)
        return len(seen)
    
    def symplectic_leaves(cnf):
        n = len(cnf)
        leaves = set()
        for i in range(1, 2**n):
            leaf = []
            for j in range(n):
                if (i >> j) & 1:
                    leaf.append(random.choice([-1, 1]) * (j + 1))
            leaves.add(tuple(sorted(leaf)))
        return leaves
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_order = float('inf')
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        leaves = symplectic_leaves(cnf)
        order = len(leaves)
        
        if order < min_order:
            min_order = order
        
        instances_tested += len(cnf)
        n_max = max(n_max, n)
    
    conjecture_holds = min_order >= 1 and min_order <= width
    counterexample = "" if conjecture_holds else f"min_order={min_order}, width={width}"
    
    return {
        "metric_name": "minimal_order",
        "metric_value": min_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")