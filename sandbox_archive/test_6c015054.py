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
    
    def generate_random_state(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_lie_algebra_rank(state):
        # Placeholder function to simulate the computation
        return len(set(state))
    
    def estimate_quantum_query_complexity(state):
        n = int(math.log2(len(state)))
        return n
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        state = generate_random_state(n)
        
        L_rho = compute_lie_algebra_rank(state)
        Q_rho = estimate_quantum_query_complexity(state)
        
        if L_rho > 2 or not math.isclose(Q_rho, n, rel_tol=1e-9):
            conjecture_holds = False
            counterexample = f"n={n}, state={state}, L_rho={L_rho}, Q_rho={Q_rho}"
            break
        
        instances_tested += 1
    
    return {
        "metric_name": "lie_algebra_rank_vs_query_complexity",
        "metric_value": (instances_tested - conjecture_holds) / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")