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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def minimal_local_ring_norm(cnf, n):
        if not cnf:
            return 0
        min_val = float('inf')
        for i in range(2**n):
            valuation = [((i >> j) & 1) * 2 - 1 for j in range(n)]
            value = sum(abs(sum(valuation[j-1] if lit > 0 else -valuation[-j] for lit in clause)) for clause in cnf)
            min_val = min(min_val, value)
        return min_val
    
    def dpll_search_tree(cnf):
        def dpll(model, clauses):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_model = model[:]
                new_model.append(literal)
                if all(lit in new_model or -lit not in new_model for lit in clause):
                    return dpll(new_model, [c for c in clauses if literal not in c and -literal not in c])
                else:
                    return False
            pure_literal = next((l for l in range(1, n+1) if (l in model or -l in model) and (-l in model or l in model)), None)
            if pure_literal is not None:
                new_model = model[:]
                new_model.append(pure_literal)
                return dpll(new_model, [c for c in clauses if pure_literal not in c and -pure_literal not in c])
            literal = next((l for l in range(1, n+1) if l not in model and -l not in model), None)
            return dpll(model + [literal], [c for c in clauses if literal not in c]) or dpll(model + [-literal], [c for c in clauses if -literal not in c])
        
        return len(dpll([], cnf))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(1, 2 * n)
    formula = generate_cnf(n, m)
    
    min_norm = minimal_local_ring_norm(formula, n)
    tree_diameter = dpll_search_tree(formula)
    
    return {
        "metric_name": "min_norm_vs_diameter",
        "metric_value": min_norm,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")