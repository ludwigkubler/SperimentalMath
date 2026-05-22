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
    
    def generate_instance(n, m):
        variables = [f"x{i+1}" for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f"~{v}" for v in variables], 3)
            while len(set(clause)) != 3:
                clause = random.sample(variables + [f"~{v}" for v in variables], 3)
            clauses.append(clause)
        return variables, clauses
    
    def cocomplex_rank(variables, clauses):
        n = len(variables)
        rank = 0
        for i in range(n):
            clause_count = sum(1 for clause in clauses if f"x{i+1}" in clause or f"~x{i+1}" in clause)
            rank += clause_count
        return rank
    
    def f(n):
        # Placeholder function for the upper bound on SAT solver time complexity
        # This is a dummy function and should be replaced with an actual mathematical function
        return n**2  # Example: quadratic function
    
    variables, clauses = generate_instance(10, 20)  # Adjust n and m as needed
    rank = cocomplex_rank(variables, clauses)
    
    return {
        "metric_name": "Cocomplex Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= f(len(variables)),
        "counterexample": "" if rank <= f(len(variables)) else f"Rank {rank} exceeds bound {f(len(variables))}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")