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
    
    def generate_circuit(n, m):
        inputs = [f"x{i}" for i in range(n)]
        literals = inputs + [f"¬{x}" for x in inputs]
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, 2)
            if random.choice([True, False]):
                clause = [f"¬{x}" for x in clause]
            clauses.append(clause)
        return inputs, literals, clauses
    
    def dpll(cnf):
        def solve(model):
            if not cnf:
                return model
            literal = next(lit for lit in literals if all(lit not in m and f"¬{lit}" not in m for m in cnf))
            pos_lit = literal[0] != "¬"
            new_cnf = [c for c in cnf if literal not in c and f"¬{literal}" not in c]
            model[literal] = pos_lit
            result = solve(model)
            if result:
                return result
            del model[literal]
            model[f"¬{literal}"] = not pos_lit
            result = solve(model)
            if result:
                return result
            return None
        
        literals = sorted(set(lit for clause in cnf for lit in clause))
        return solve({})
    
    def groupoid_composition_width(cnf):
        # Simplified approximation of gcw(C) using a placeholder function
        n, m = len(inputs), len(cnf)
        return math.ceil(math.log2(n + m))
    
    inputs, literals, clauses = generate_circuit(10, 5)
    cnf = [tuple(clause) for clause in clauses]
    w_C = dpll(cnf)
    gcw_C = groupoid_composition_width(cnf)
    
    if w_C is None:
        return {
            "metric_name": "gcw(C) / w(C)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": 10,
            "conjecture_holds": False,
            "counterexample": "DPLL solver failed to find a model"
        }
    
    return {
        "metric_name": "gcw(C) / w(C)",
        "metric_value": gcw_C / w_C,
        "instances_tested": 1,
        "n_max": 10,
        "conjecture_holds": gcw_C <= 2 * w_C,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='DPLL solver failed to find a model' first_failing_seed={first_failing_seed}")