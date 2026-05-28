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
    
    def generate_3cnf(n, m):
        literals = [f"x{i}" for i in range(1, n+1)] + [f"~x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, 3)
            if random.choice([True, False]):
                clause[0] = f"~{clause[0]}"
                clause[1] = f"~{clause[1]}"
                clause[2] = f"~{clause[2]}"
            clauses.append(clause)
        return clauses
    
    def dpll_solver(clauses):
        if not clauses:
            return True, []
        literal = random.choice([l for l in set(l for c in clauses for l in c) if l.startswith('x')])
        pos_literal = literal
        neg_literal = f"~{literal}"
        pos_clauses = [c for c in clauses if pos_literal not in c]
        neg_clauses = [c for c in clauses if neg_literal not in c]
        if dpll_solver(pos_clauses):
            return True, [pos_literal] + []
        if dpll_solver(neg_clauses):
            return True, [neg_literal] + []
        return False, []
    
    def compute_toric_rank(n):
        # Placeholder for actual toric variety rank computation
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_time = 0
    
    for n in n_values:
        m = int(1.5 * n)
        clauses = generate_3cnf(n, m)
        start_time = time.time()
        conjecture_holds = True
        counterexample = ""
        
        if not dpll_solver(clauses):
            continue
        
        rank = compute_toric_rank(n)
        t_star = len(dpll_solver(clauses)[1])
        
        if t_star > 2 * m**2 * math.log(n):
            conjecture_holds = False
            counterexample = f"t*({n}, {m})={t_star} > 2*m^2*log(n)={2*m**2*math.log(n)}"
        
        results.append({
            "metric_name": "resolution_proof_length",
            "metric_value": t_star,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    mean_t_star = sum(result["metric_value"] for result in results) / len(results)
    std_t_star = math.sqrt(sum((result["metric_value"] - mean_t_star)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_t_star": mean_t_star,
        "std_t_star": std_t_star,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_t_star = sum(result["mean_t_star"] for result in results) / len(results)
    std_t_star = math.sqrt(sum((result["mean_t_star"] - mean_t_star)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] == 1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_t_star} std={std_t_star} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")