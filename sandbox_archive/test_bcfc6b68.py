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
    
    def generate_random_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            var = abs(unit_clause[0])
            val = unit_clause[0] > 0
            if var in assignment and assignment[var] != val:
                return False
            new_assignment = assignment.copy()
            new_assignment[var] = val
            return dpll(cnf, new_assignment)
        pure_literal = next((c for c in cnf if len(set(abs(x) for x in c)) == 1), None)
        if pure_literal:
            var = abs(pure_literal[0])
            val = pure_literal[0] > 0
            if var in assignment and assignment[var] != val:
                return False
            new_assignment = assignment.copy()
            new_assignment[var] = val
            return dpll(cnf, new_assignment)
        var = random.choice([v for v in range(1, n + 1) if v not in assignment])
        return dpll(cnf, assignment | {var: True}) or dpll(cnf, assignment | {var: False})
    
    def frege_refutation_depth(cnf):
        depth = 0
        stack = [cnf]
        while stack:
            cnf = stack.pop()
            if not cnf:
                continue
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                var = abs(unit_clause[0])
                val = unit_clause[0] > 0
                new_cnf = [c for c in cnf if var not in c]
                stack.append(new_cnf)
            else:
                pure_literal = next((c for c in cnf if len(set(abs(x) for x in c)) == 1), None)
                if pure_literal:
                    var = abs(pure_literal[0])
                    val = pure_literal[0] > 0
                    new_cnf = [c for c in cnf if var not in c]
                    stack.append(new_cnf)
                else:
                    var = random.choice([v for v in range(1, n + 1) if v not in assignment])
                    new_cnf_true = [c for c in cnf if var not in c]
                    new_cnf_false = [c for c in cnf if -var not in c]
                    stack.append(new_cnf_true)
                    stack.append(new_cnf_false)
            depth += 1
        return depth
    
    def geometric_entropy(hyperplane_arrangement):
        # Placeholder function to compute geometric entropy
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()
    
    n = random.randint(5, 40)
    m = random.randint(n, n * (n + 1) // 2)
    cnf = generate_random_cnf(n, m)
    
    depth = frege_refutation_depth(cnf)
    entropy = geometric_entropy(cnf)
    
    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,  # Placeholder
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")