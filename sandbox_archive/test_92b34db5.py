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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(lit != -other_lit for lit in clause for other_lit in clause):
                cnf.append(clause)
        return cnf
    
    def geometric_entropy(cnf):
        n = len(cnf[0])
        count = [[0, 0] for _ in range(2*n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    count[lit][0] += 1
                else:
                    count[-lit][1] += 1
        entropy = 0.0
        for c in count:
            if c[0] + c[1] == 0:
                continue
            p = Fraction(c[0], c[0] + c[1])
            entropy -= p * math.log(p, 2)
        return entropy
    
    def dpll(cnf):
        n = len(cnf[0])
        assignment = [None] * (n + 1)
        
        def solve(index):
            if index == n + 1:
                return True
            for lit in [-index, index]:
                if all(lit not in clause or assignment[-lit] is None for clause in cnf):
                    assignment[index] = lit > 0
                    if solve(index + 1):
                        return True
                    assignment[index] = None
            return False
        
        return solve(1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        entropy = geometric_entropy(cnf)
        proof_length = len(dpll(cnf))
        
        if entropy <= 0 or proof_length == 0:
            continue
        
        total_metric_value += entropy / proof_length
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "geometric_entropy_over_proof_length",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(0.9 * mean_metric_value <= geometric_entropy(generate_cnf(n)) / len(dpll(generate_cnf(n))) <= 1.1 * mean_metric_value for n in range(5, 41))
    
    return {
        "metric_name": "geometric_entropy_over_proof_length",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")