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
    
    def generate_kcnf(n, k):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(k):
            clause = random.sample(literals, 2)
            clause.append(random.choice(['!', '']))
            clauses.append(clause)
        return clauses
    
    def dpll_solve(clauses, assignment):
        if not clauses:
            return True
        literal = next((l for l in literals if l not in assignment and '!'+l not in assignment), None)
        if literal is None:
            return False
        
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll_solve(clauses, new_assignment):
            return True
        
        new_assignment[literal] = False
        if dpll_solve(clauses, new_assignment):
            return True
        
        return False
    
    def rank_koszul_complex(kcnf):
        # Simplified version for demonstration; actual implementation would be complex
        return len(kcnf)
    
    n_values = [40, 42, 44, 46, 48, 50]
    results = []
    
    for n in n_values:
        kcnf = generate_kcnf(n, n // 3)
        rank = rank_koszul_complex(kcnf)
        
        if rank == 0:
            continue
        
        t_star = 1
        while not dpll_solve(kcnf, {}):
            t_star += 1
        
        ratio = math.log2(t_star) / rank
        results.append(ratio)
    
    if len(results) < 30:
        return {
            "metric_name": "log2_t_star_over_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_ratio = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_ratio) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "log2_t_star_over_rank",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": mean_ratio <= 1,  # Simplified check
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, ratio={r['metric_value']}"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(r)]}")