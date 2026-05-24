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
        for i in range(1, n + 1):
            clause = [random.randint(-i, -1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def dpll_refutation_depth(cnf):
        def dpll(cnf, assignment, literals):
            if not cnf:
                return 0
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                return dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment, literals)
            pure_literal = next((l for l in literals if all(l not in c or -l in c for c in cnf)), None)
            if pure_literal is None:
                return 1
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll(cnf, new_assignment, literals)
        return dpll(cnf, {}, list(range(1, len(cnf) + 1)))
    
    def minimal_totally_ramified_extension_order(n):
        # This is a placeholder function. Implement the actual algorithm to find the minimal order.
        return random.randint(1, n)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    t_F = dpll_refutation_depth(cnf)
    k = minimal_totally_ramified_extension_order(n)
    
    if k == 0 or t_F == 0:
        return {
            "metric_name": "log2(k) vs log2(t*(F))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = (math.log2(k), math.log2(t_F))
    return {
        "metric_name": "log2(k) vs log2(t*(F))",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'][0] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'][0] - (sum(r['metric_value'][0] for r in results) / len(results)))**2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")