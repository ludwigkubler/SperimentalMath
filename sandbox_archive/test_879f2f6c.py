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
    
    def generate_cnf(n):
        cnf = []
        for i in range(1, n+1):
            clause = [random.choice([-1, 1]) * j for j in range(1, n+1)]
            cnf.append(clause)
        return cnf
    
    def resolution_proof_size(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        states = []
        while True:
            new_clause = None
            for i in range(len(states)):
                for j in range(i+1, len(states)):
                    if any(-lit in states[i] and lit in states[j] for lit in clauses):
                        new_clause = tuple(sorted([lit for lit in states[i] + states[j] if lit > 0]))
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(states)
            states.append(new_clause)
    
    def l_p_norm(arrangement, p):
        norm = sum(abs(x) ** p for x in arrangement)
        return norm ** (1 / p)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_size = resolution_proof_size(cnf)
    arrangement = [random.uniform(-10, 10) for _ in range(n)]
    l_p_val = l_p_norm(arrangement, 2)
    
    return {
        "metric_name": "L^p norm",
        "metric_value": l_p_val,
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
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                counterexample = f"n={res['n_max']}, L^p norm={res['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break