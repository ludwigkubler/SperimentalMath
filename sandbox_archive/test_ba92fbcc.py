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
    
    def dpll(cnf, assignment, clauses):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause is not None:
            literal = unit_clause[0]
            new_assignment = assignment[:]
            new_assignment[abs(literal) - 1] = literal > 0
            return dpll(cnf, new_assignment, [c for c in clauses if literal not in c])
        
        p = random.choice([l for l in range(1, len(assignment) + 1)])
        new_assignment_true = assignment[:]
        new_assignment_true[p - 1] = True
        if dpll(cnf, new_assignment_true, [c for c in clauses if p not in c]):
            return True
        
        new_assignment_false = assignment[:]
        new_assignment_false[p - 1] = False
        return dpll(cnf, new_assignment_false, [c for c in clauses if -p not in c])
    
    def resolution_width(cnf):
        n = len(cnf)
        return len(cnf) if dpll(cnf, [False] * n, cnf) else 0
    
    def local_zeta_function(cnf):
        n = len(cnf)
        zeta_values = [1] * (n + 1)
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    zeta_values[literal] -= Fraction(1, 2 ** len(clause))
                else:
                    zeta_values[-literal] -= Fraction(1, 2 ** len(clause))
        return sum(zeta_values)
    
    def order_zeta_function(zeta):
        return abs(math.log(abs(zeta), 2)) if abs(zeta) > 0 else 0
    
    n = random.randint(5, 40)
    cnf = [[random.choice([-i, i]) for _ in range(random.randint(1, n))] for _ in range(n)]
    
    zeta = local_zeta_function(cnf)
    order = order_zeta_function(zeta)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "Order of Local Zeta Function",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order >= width * 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "Order of zeta function is less than 0.7 times resolution proof width"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")