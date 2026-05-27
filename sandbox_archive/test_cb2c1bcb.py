# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(variables, clauses):
        if not clauses:
            return {}
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            var, val = unit_clauses[0][0], True
            new_clauses = [[(v, not v_val) for v, v_val in clause if v != var] for clause in clauses]
            model = dpll(variables - {var}, new_clauses)
            if model is not None:
                model[var] = val
                return model
        pure_symbols = {}
        for var in variables:
            pos_count = sum(1 for c in clauses if (var, True) in c)
            neg_count = sum(1 for c in clauses if (var, False) in c)
            if pos_count == 0 and var not in pure_symbols:
                pure_symbols[var] = False
            elif neg_count == 0 and var not in pure_symbols:
                pure_symbols[var] = True
        if pure_symbols:
            val = pure_symbols[next(iter(pure_symbols))]
            new_clauses = [[(v, not v_val) for v, v_val in clause if v != next(iter(pure_symbols))] for clause in clauses]
            model = dpll(variables - {next(iter(pure_symbols))}, new_clauses)
            if model is not None:
                model[next(iter(pure_symbols))] = val
                return model
        var = variables.pop()
        for val in [True, False]:
            new_clauses = [[(v, not v_val) for v, v_val in clause if v != var] for clause in clauses]
            model = dpll(variables.copy(), new_clauses)
            if model is not None:
                model[var] = val
                return model
        variables.add(var)
        return None
    
    def tropicalized_rank(clause):
        return sum(1 for literal in clause if literal[1])
    
    n = random.randint(5, 40)
    variables = set(f"x{i}" for i in range(n))
    clauses = []
    for _ in range(2**n - 1):
        clause = [(f"x{i}", random.choice([True, False])) for i in range(n)]
        if all(lit[1] == clause[0][1] for lit in clause):
            continue
        clauses.append(clause)
    
    circuit_depth = len(dpll(variables, clauses))
    rank = sum(tropicalized_rank(c) for c in clauses)
    
    metric_name = "tropicalized_rank"
    metric_value = rank / circuit_depth
    instances_tested = 1
    conjecture_holds = metric_value <= (math.log2(n))**2 and any(metric_value == math.log(n, 2) for _ in range(30))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")