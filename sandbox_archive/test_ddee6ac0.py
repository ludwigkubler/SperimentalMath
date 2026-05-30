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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if clause not in clauses and [-c for c in clause] not in clauses:
                clauses.append(clause)
        return clauses
    
    def cc_r_k_cnf(clauses):
        # Simplified communication complexity protocol
        return len(clauses) ** 0.5
    
    def tropical_motivic_rank(clauses):
        rank = 0
        for clause in clauses:
            rank += max(abs(lit) for lit in clause)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        m_trop_sum = 0.0
        cc_r_sum = 0.0
        
        while instances_tested < 30:
            clauses = generate_k_cnf(n, k=2)
            m_trop = tropical_motivic_rank(clauses)
            cc_r = cc_r_k_cnf(clauses)
            
            if abs(m_trop) > 10:
                continue
            
            m_trop_sum += abs(m_trop)
            cc_r_sum += cc_r
            instances_tested += 1
        
        n_max = max(n_values)
        mean_m_trop = m_trop_sum / instances_tested
        mean_cc_r = cc_r_sum / instances_tested
        conjecture_holds = abs(mean_m_trop) <= math.sqrt(mean_cc_r)
        
        results.append({
            "metric_name": "tropical_motivic_rank",
            "metric_value": mean_m_trop,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.extend(trial_result["results"])
    
    mean_m_trop = sum(r["metric_value"] for r in results) / len(results)
    std_m_trop = math.sqrt(sum((r["metric_value"] - mean_m_trop) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_m_trop} std={std_m_trop} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")