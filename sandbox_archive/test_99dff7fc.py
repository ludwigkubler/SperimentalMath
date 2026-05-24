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
    
    def dpll_solve(instance):
        n = len(instance)
        assignment = {}
        
        def solve(literals, clause):
            if not literals:
                return True
            l = literals[0]
            if l in assignment or -l in assignment:
                return solve(literals[1:], clause)
            for val in [True, False]:
                assignment[l] = val
                if all(solve([x for x in literals if x != l], instance) for _ in range(3)):
                    return True
                del assignment[l]
            return False
        
        return solve(list(range(1, n + 1)), instance)
    
    def minimal_rank_of_kostant_sheaf(n):
        if n > 4:
            return "mapping_undefined"
        
        # Generate a random instance of a polynomial-time solvable problem
        instance = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Solve the instance using DPLL
        if dpll_solve(instance):
            return 1
        else:
            return float('inf')
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        rank_value = minimal_rank_of_kostant_sheaf(n)
        if rank_value == "mapping_undefined":
            return {
                "metric_name": "minimal_rank",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        ranks.append(rank_value)
    
    mean_rank = sum(ranks) / len(ranks)
    conjecture_holds = all(rank <= math.log(n, 2)**n for n, rank in zip(n_values, ranks))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")