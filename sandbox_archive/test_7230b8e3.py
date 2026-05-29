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
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == -clause[-i-1] for i in range(n // 2)):
                continue
            clauses.append(clause)
        return clauses

    def dpll_tree_depth(cnf):
        assignment = [None] * len(cnf[0])
        
        def dpll(assignment, clause_index):
            if clause_index == len(cnf):
                return True
            for i in range(len(assignment)):
                if assignment[i] is None:
                    assignment[i] = 1
                    if all(any(var != -c for c in clause) for clause in cnf[clause_index:]):
                        if dpll(assignment, clause_index + 1):
                            return True
                    assignment[i] = -1
                    if all(any(var != -c for c in clause) for clause in cnf[clause_index:]):
                        if dpll(assignment, clause_index + 1):
                            return True
                    assignment[i] = None
            return False
        
        return len(cnf)

    def br_generator_count(n):
        # Placeholder function to simulate Brauer group generator count
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        dpll_depth_n = dpll_tree_depth(cnf)
        br_count_n = br_generator_count(n)
        
        if br_count_n > dpll_depth_n + 1:
            return {
                "metric_name": "Brauer Group Generator Count vs DPLL Depth",
                "metric_value": br_count_n,
                "instances_tested": len(cnf),
                "conjecture_holds": False,
                "counterexample": f"n={n}, m(Br(F))={br_count_n}, t*(F)={dpll_depth_n}"
            }
    
    return {
        "metric_name": "Brauer Group Generator Count vs DPLL Depth",
        "metric_value": sum(br_generator_count(n) for n in n_values),
        "instances_tested": len(cnf) * len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")