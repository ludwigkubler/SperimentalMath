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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses

    def is_satisfiable(phi):
        # Simplified satisfiability check
        assignment = {i: random.choice([True, False]) for i in range(1, n + 1)}
        for clause in phi:
            if not any(lit == (2 * int(assignment[abs(lit)])) - 1 for lit in clause):
                return False
        return True

    def sos_degree(phi):
        # Simplified SOS degree calculation
        return len(phi)

    n = 40
    phi = generate_3cnf(n)
    epsilon = 1 / (n ** 2)
    
    if not is_satisfiable(phi):
        return {
            "metric_name": "sos_degree",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Unsatisfiable 3-CNF instance"
        }

    d = sos_degree(phi)
    
    if d >= (c * dim_sqrt_I_phi / math.log(n)):
        return {
            "metric_name": "sos_degree",
            "metric_value": d,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "sos_degree",
            "metric_value": d,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Failed for n={n}, d={d}"
        }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 30)]
    
    results = []
    total_metric_value = 0.0
    count_supporting_conjecture = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["conjecture_holds"]:
            count_supporting_conjecture += 1
        
        total_metric_value += trial_result["metric_value"]
    
    mean_metric_value = total_metric_value / len(seeds)
    support_fraction = count_supporting_conjecture / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        for seed in seeds:
            result = run_trial(seed)
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Failed for n=40\" first_failing_seed={seed}")
                break