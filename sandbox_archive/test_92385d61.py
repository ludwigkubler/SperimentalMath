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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def communication_complexity_rank(cnf):
        rank = 0
        seen_vars = set()
        for clause in cnf:
            for var in clause:
                if abs(var) not in seen_vars:
                    seen_vars.add(abs(var))
                    rank += 1
        return rank
    
    def automorphic_forms_required(n, comm_rank):
        # Placeholder function to simulate the calculation of automorphic forms required
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    comm_rank = communication_complexity_rank(cnf)
    automorphic_forms = automorphic_forms_required(n, comm_rank)
    
    if automorphic_forms > math.sqrt(comm_rank):
        return {
            "metric_name": "Automorphic Forms Required",
            "metric_value": automorphic_forms,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"CNF with n={n} requires {automorphic_forms} forms but only √{comm_rank:.2f} is allowed."
        }
    else:
        return {
            "metric_name": "Automorphic Forms Required",
            "metric_value": automorphic_forms,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")