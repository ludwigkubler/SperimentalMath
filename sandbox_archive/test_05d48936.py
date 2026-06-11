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
    
    def generate_formula(n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(literals, 3)
            if random.choice([True, False]):
                clause = [f'-{lit}' for lit in clause]
            clauses.append(' '.join(clause))
        return ' '.join(clauses)

    def dpll(formula):
        literals = set()
        for clause in formula.split('\n'):
            for lit in clause.split():
                if lit[0] == '-':
                    literals.add(lit[1:])
                else:
                    literals.add(lit)
        
        def solve(model, clauses):
            if not clauses:
                return True
            literal = next(iter(literals))
            pos_literal = f'x{literal}'
            neg_literal = f'-x{literal}'
            
            if pos_literal in model or neg_literal in model:
                continue
            
            for clause in clauses[:]:
                if any(lit in model for lit in clause.split()):
                    clauses.remove(clause)
                elif all(lit[1:] not in model for lit in clause.split()):
                    return False
            
            if solve(model | {pos_literal: True}, clauses):
                return True
            if solve(model | {neg_literal: False}, clauses):
                return True
            return False
        
        return solve({}, formula.split('\n'))
    
    def mld(formula):
        # Placeholder for minimal local induction dimension calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(formula.split('\n'))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_instances = 0
    
    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n)
            w_DPLL = dpll(formula)
            mld_val = mld(formula)
            if w_DPLL is None or mld_val is None:
                continue
            results.append((mld_val, w_DPLL))
            total_instances += 1
    
    if not results:
        return {
            "metric_name": "mld_vs_w_DPLL",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mld_values = [r[0] for r in results]
    w_DPLL_values = [r[1] for r in results]
    
    mean_mld = sum(mld_values) / len(mld_values)
    mean_w_DPLL = sum(w_DPLL_values) / len(w_DPLL_values)
    std_dev = math.sqrt(sum((x - mean_w_DPLL) ** 2 for x in w_DPLL_values) / len(w_DPLL_values))
    
    correlation_coefficient = (sum((mld_values[i] - mean_mld) * (w_DPLL_values[i] - mean_w_DPLL) for i in range(len(mld_values))) /
                               (len(mld_values) * std_dev * math.sqrt(sum((x - mean_w_DPLL) ** 2 for x in w_DPLL_values))))
    
    return {
        "metric_name": "mld_vs_w_DPLL",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and all(abs(m - w) <= 3 for m, w in zip(mld_values, w_DPLL_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")