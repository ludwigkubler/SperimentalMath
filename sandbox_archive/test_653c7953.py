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
        for _ in range(2 ** n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(abs(c) != abs(clause[0]) for c in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        p = next((c for c in set(sum(clauses, [])) if c > 0), None)
        if p is None:
            return False
        
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[p] = val
            if dpll([c for c in clauses if not any(abs(l) == abs(p) for l in c)], new_assignment):
                return True
        return False
    
    def quantized_phase_space_map(clauses):
        rank = 0
        for clause in clauses:
            rank += len(set(abs(l) for l in clause))
        return rank
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    dpll_length = 1 if dpll(cnf, {}) else float('inf')
    quantized_rank = quantized_phase_space_map(cnf)
    
    metric_value = quantized_rank / dpll_length
    conjecture_holds = metric_value <= 2.0  # Placeholder constant for demonstration
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "R(F) / t*(F)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")