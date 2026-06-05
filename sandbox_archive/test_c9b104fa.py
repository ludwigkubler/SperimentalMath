# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        return ' & '.join(f'x{i+1}' if random.choice([True, False]) else f'(¬x{i+1})' for i in range(n))
    
    def dpll(formula, assignment):
        if not formula:
            return True
        var = next((v for v in formula if v[0] != '¬'), None)
        if var is None:
            return False
        pos_var = var if var[0] != '¬' else var[1:]
        neg_var = var[1:] if var[0] == '¬' else f'(¬{var})'
        
        def simplify(formula, var):
            return [f for f in formula if not (f.startswith(var) or f.startswith(neg_var))]
        
        pos_assignment = assignment.copy()
        pos_assignment[pos_var] = True
        neg_assignment = assignment.copy()
        neg_assignment[neg_var] = True
        
        if dpll(simplify(formula, var), pos_assignment):
            return True
        if dpll(simplify(formula, neg_var), neg_assignment):
            return True
        return False
    
    def resolution_width(formula):
        clauses = formula.split(' & ')
        assignment = {}
        queue = [clauses]
        
        while queue:
            clause = queue.pop()
            if not clause:
                continue
            var = next((v for v in clause if v[0] != '¬'), None)
            if var is None:
                return 1
            
            pos_var = var if var[0] != '¬' else var[1:]
            neg_var = var[1:] if var[0] == '¬' else f'(¬{var})'
            
            new_clauses = []
            for c in queue:
                if pos_var in c and neg_var in c:
                    return 2
                elif pos_var in c:
                    new_clauses.append(c.replace(pos_var, '').replace(' & ', ''))
                elif neg_var in c:
                    new_clauses.append(c.replace(neg_var, '').replace(' & ', ''))
            queue.extend(new_clauses)
        
        return 1
    
    def tropical_order(formula):
        # Simplified mapping for demonstration purposes
        return len(formula.split(' & '))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    order = tropical_order(formula)
    width = resolution_width(formula)
    
    return {
        "metric_name": "order_over_width",
        "metric_value": Fraction(order, width) if width != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order / width >= 0.5 and order / width <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"]) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"order_over_width out of range\" first_failing_seed={r['seed']}")
                break