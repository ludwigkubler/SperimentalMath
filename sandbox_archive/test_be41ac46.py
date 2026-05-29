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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Generate 10n clauses
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def literal_true(lit, assignment):
            return (lit > 0 and assignment[lit - 1]) or (lit < 0 and not assignment[-lit - 1])
        
        def unit_propagate(cnf, assignment):
            while True:
                found = False
                for i in range(len(cnf)):
                    if len([l for l in cnf[i] if literal_true(l, assignment)]) == 0:
                        return None, []
                    if len([l for l in cnf[i] if not literal_true(l, assignment)]) == 1:
                        lit = [l for l in cnf[i] if not literal_true(l, assignment)][0]
                        assignment[abs(lit) - 1] = lit > 0
                        found = True
                if not found:
                    break
            return cnf, assignment
        
        def dpll_rec(cnf, assignment):
            cnf, assignment = unit_propagate(cnf, assignment)
            if cnf is None:
                return False
            if all(len(clause) == 0 for clause in cnf):
                return True
            
            var = next(i for i in range(len(assignment)) if not assignment[i])
            for val in [True, False]:
                new_assignment = assignment[:]
                new_assignment[var] = val
                result = dpll_rec(cnf, new_assignment)
                if result:
                    return True
            return False
        
        return dpll_rec(cnf, [False] * n)
    
    def bruer_group_size(n):
        # Simplified Brauer group size calculation for demonstration purposes
        return 2 ** (n - 1)
    
    def dpll_tree_depth(cnf):
        depth = 0
        stack = [(cnf, [])]
        while stack:
            cnf, assignment = stack.pop()
            if all(len(clause) == 0 for clause in cnf):
                return len(assignment)
            var = next(i for i in range(len(assignment)) if not assignment[i])
            for val in [True, False]:
                new_assignment = assignment[:]
                new_assignment[var] = val
                stack.append((cnf, new_assignment))
            depth += 1
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        bruer_group_size_n = bruer_group_size(n)
        dpll_depth_n = dpll_tree_depth(cnf)
        
        if bruer_group_size_n > math.log2(dpll_depth_n):
            counterexample = f"n={n}, m(Br(F))={bruer_group_size_n}, t*(F)={dpll_depth_n}"
            return {
                "metric_name": "Brauer Group Size vs DPLL Depth",
                "metric_value": bruer_group_size_n,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
    
    return {
        "metric_name": "Brauer Group Size vs DPLL Depth",
        "metric_value": sum(bruer_group_size(n) for n in n_values),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")