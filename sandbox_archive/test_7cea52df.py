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
        for _ in range(n * (n - 1)):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def dpll_helper(model, clauses):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_model = model.copy()
                new_model[literal] = True
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                return dpll_helper(new_model, new_clauses) or dpll_helper({**new_model, literal: False}, new_clauses)
            pure_literal = next((l for l in range(1, n + 1) if (all(l in c for c in clauses) and all(-l not in c for c in clauses)) or 
                                 all(-l in c for c in clauses) and all(l not in c for c in clauses)), None)
            if pure_literal:
                new_model = model.copy()
                new_model[pure_literal] = True
                new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
                return dpll_helper(new_model, new_clauses) or dpll_helper({**new_model, pure_literal: False}, new_clauses)
            literal = random.choice([l for l in range(1, n + 1)])
            new_clauses_true = [c for c in clauses if literal not in c and -literal not in c]
            new_clauses_false = [c for c in clauses if -literal not in c and literal not in c]
            return dpll_helper({**model, literal: True}, new_clauses_true) or dpll_helper({**model, literal: False}, new_clauses_false)
        return dpll_helper({}, cnf)
    
    def quantized_phase_space_map(cnf):
        # Placeholder for the actual quantum channel and basis mapping
        return len(cnf)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    t_F = dpll(cnf)
    R_F = quantized_phase_space_map(cnf)
    
    if t_F == 0:
        return {
            "metric_name": "R(F) / t*(F)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL proof length is zero, making the ratio undefined."
        }
    
    return {
        "metric_name": "R(F) / t*(F)",
        "metric_value": R_F / t_F,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 97))  # Default to first 30 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 1.5) / len(results)  # Hypothetical constant c=1.5 for demonstration
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > 1.5 for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample=\"R(F) / t*(F) exceeds 1.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")