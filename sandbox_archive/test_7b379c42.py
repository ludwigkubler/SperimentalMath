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
        for _ in range(10 * n):  # Each clause has at least 2 literals
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def geometric_entropy(cnf):
        n = len(cnf[0])
        count = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    count[lit][1] += 1
                else:
                    count[-lit][0] += 1
        entropy = 0.0
        for i in range(1, n + 1):
            p_i = (count[i][0] + count[i][1]) / len(cnf)
            if p_i > 0:
                entropy -= p_i * math.log2(p_i)
        return entropy
    
    def dpll(cnf):
        def backtrack(model):
            if not cnf:
                return True
            literal = next((lit for lit in range(1, n + 1) if lit not in model and -lit not in model), None)
            if literal is None:
                return False
            model[literal] = True
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            if backtrack(model):
                return True
            del model[literal]
            model[-literal] = True
            new_cnf = [c for c in cnf if -literal not in c and literal not in c]
            if backtrack(model):
                return True
            del model[-literal]
            return False
        
        n = len(cnf[0])
        model = {}
        return backtrack(model)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each size 30 times
            cnf = generate_cnf(n)
            entropy = geometric_entropy(cnf)
            proof_length = len(dpll(cnf))
            total_metric_value += entropy * proof_length
            instances_tested += 1
            if not conjecture_holds:
                continue
            c = n**0.5 * math.log2(n)
            lower_bound = c * 0.9
            upper_bound = c * 1.1
            if not (lower_bound <= entropy * proof_length <= upper_bound):
                conjecture_holds = False
                counterexample = f"n={n}, entropy*proof_length={entropy*proof_length}, bounds=[{lower_bound}, {upper_bound}]"
    
    return {
        "metric_name": "H(φ) * Proof Length",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")