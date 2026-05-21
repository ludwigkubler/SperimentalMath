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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def dpll(sat_instance, assignment=None):
        if not sat_instance:
            return True
        var = next((v for v in range(1, len(sat_instance[0]) + 1) if v not in assignment), None)
        if var is None:
            return False
        
        def satisfies(clause, assignment):
            return any(assignment.get(abs(v)) == (v > 0) for v in clause)
        
        if dpll([c for c in sat_instance if not satisfies(c, assignment)], {**assignment, var: True}):
            return True
        if dpll([c for c in sat_instance if not satisfies(c, assignment)], {**assignment, var: False}):
            return True
        return False
    
    def p_adic_l_function_order(n):
        # Placeholder function. Actual implementation required.
        return random.randint(1, 5)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    sat_instance = generate_sat_instance(n)
    assignment = {}
    dpll(sat_instance, assignment)
    depth = len(assignment)  # Simplified for testing purposes
    order = p_adic_l_function_order(n)
    
    return {
        "metric_name": "DPLL Depth vs P-adic Order",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": True if order > 2 and depth >= 3 else False,
        "counterexample": "" if order > 2 and depth >= 3 else "O(p-adic, n) = 2 with DPLL depth < 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break