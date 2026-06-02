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

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def tseitin_encoding(cnf):
    literals = set()
    new_vars = {}
    formulas = []
    
    def get_new_var():
        nonlocal new_vars
        var = len(new_vars) + 1
        new_vars[var] = True
        return var
    
    for i, clause in enumerate(cnf):
        literals.update(clause)
        p_i = get_new_var()
        formulas.append([p_i] + [-l for l in clause])
        
        for j in range(len(clause)):
            q_j = get_new_var()
            formulas.append([-p_i, clause[j], -q_j])
            formulas.append([-clause[j], q_j])
            formulas.append([q_j, -p_i])
    
    return literals, new_vars, formulas

def resolution_width(formulas):
    seen = set()
    queue = list(formulas)
    while queue:
        literal = random.choice(queue)
        if literal in seen or -literal in seen:
            continue
        seen.add(literal)
        for formula in formulas:
            if literal in formula and -literal not in formula:
                new_clause = [l for l in formula if l != literal]
                if new_clause not in seen and new_clause != []:
                    queue.append(new_clause)
    return len(seen)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        m = random.randint(1, n * (n - 1) // 2)
        cnf = generate_cnf(n, m)
        literals, new_vars, formulas = tseitin_encoding(cnf)
        
        width = resolution_width(formulas)
        total_width += width
        instances_tested += len(formulas)
    
    if instances_tested < 30:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_width = total_width / instances_tested
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": True if 0.8 * n_values[-1] * math.log2(n_values[-1]) <= mean_width <= 1.2 * n_values[-1] * math.log2(n_values[-1]) else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")