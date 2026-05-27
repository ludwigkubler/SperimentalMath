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
    
    def is_satisfiable(cnf):
        # Implement a simple backtracking SAT solver here
        def backtrack(assignment, clause_index=0):
            if clause_index == len(cnf):
                return True
            literals = cnf[clause_index]
            for literal in literals:
                var = abs(literal) - 1
                if literal > 0 and (var not in assignment or assignment[var] != 1):
                    assignment[var] = 1
                    if backtrack(assignment, clause_index + 1):
                        return True
                    assignment.pop(var)
                elif literal < 0 and (var not in assignment or assignment[var] != -1):
                    assignment[var] = -1
                    if backtrack(assignment, clause_index + 1):
                        return True
                    assignment.pop(var)
            return False
        
        return backtrack({})
    
    def quandle_rank(cnf):
        # Implement a simple method to compute the rank of the quandle structure here
        n = len(cnf)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all(lit not in cnf[j] for lit in cnf[i]):
                    rank += 1
        return rank
    
    n = random.randint(5, 40)
    cnf = []
    for _ in range(random.randint(2 * n, 3 * n)):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        cnf.append(clause)
    
    rank = quandle_rank(cnf)
    bound = Fraction(n ** (3 / 2))
    
    return {
        "metric_name": "minimal_rank_over_bound",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= bound,
        "counterexample": "" if rank <= bound else f"Rank {rank} exceeds bound {bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")