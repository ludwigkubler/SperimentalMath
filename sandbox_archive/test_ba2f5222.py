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
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(-1, 1) * (i + 1) for i in range(n)]
            if any(x == 0 for x in clause):
                continue
            cnf.append(clause)
        return cnf
    
    def resolution_proof_size(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        resolvents = []
        while True:
            new_resolvent = False
            for i in range(len(resolvents)):
                for j in range(i + 1, len(resolvents)):
                    common = [x for x in resolvents[i] if -x in resolvents[j]]
                    if common:
                        new_clause = sorted(set(resolvents[i]) | set(resolvents[j]) - {common[0], -common[0]})
                        if new_clause not in clauses and new_clause not in resolvents:
                            resolvents.append(new_clause)
                            new_resolvent = True
            if not new_resolvent:
                break
        return len(resolvents)
    
    def l_p_norm(arrangement, p):
        norm = 0
        for line in arrangement:
            norm += sum(abs(x) ** p for x in line) ** (1 / p)
        return norm
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    t_star = resolution_proof_size(cnf)
    
    if t_star == 0:
        return {
            "metric_name": "L_p_norm",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_size_is_zero"
        }
    
    arrangement = []
    for clause in cnf:
        line = [random.uniform(-1, 1) for _ in range(n + 1)]
        if all(line[i] * (x if x > 0 else -x) >= 0 for x in clause):
            continue
        arrangement.append(line)
    
    if not arrangement:
        return {
            "metric_name": "L_p_norm",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "no_valid_arrangement_found"
        }
    
    metric_value = l_p_norm(arrangement, random.choice([1, 2]))
    return {
        "metric_name": "L_p_norm",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first_failing_seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")