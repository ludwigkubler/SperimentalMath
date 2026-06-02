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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            cnf.append(clause)
        return cnf
    
    def min_order(cnf):
        n = len(cnf[0])
        truth_table = [sum([lit if val > 0 else -lit for lit, val in zip(row, assignment)]) for row in cnf]
        degree = 1
        while True:
            all_zero = True
            for i in range(degree):
                if sum(truth_table[j] * (i + 1) ** j for j in range(len(truth_table))) != 0:
                    all_zero = False
                    break
            if all_zero:
                return degree
            degree += 1
    
    def frege_proof_length(cnf):
        # Simplified DPLL solver to estimate proof length
        assignment = [None] * len(cnf[0])
        stack = []
        for clause in cnf:
            literals = [lit for lit, val in zip(clause, assignment) if val is None]
            if not literals:
                return 1
            literal = random.choice(literals)
            assignment[literal - 1] = 1 if literal > 0 else -1
            stack.append((clause, literal))
        while stack:
            clause, literal = stack.pop()
            new_clause = [lit for lit in clause if lit != literal and lit != -literal]
            if not new_clause:
                return len(cnf) + 1
            literals = [lit for lit, val in zip(new_clause, assignment) if val is None]
            if not literals:
                return len(cnf) + 2
            literal = random.choice(literals)
            assignment[literal - 1] = 1 if literal > 0 else -1
            stack.append((new_clause, literal))
        return len(cnf) + 3
    
    def f(n):
        return n ** (math.log(n) / math.log(math.log(n)))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        min_order_value = min_order(cnf)
        proof_length = frege_proof_length(cnf)
        results.append({
            "n": n,
            "min_order": min_order_value,
            "proof_length": proof_length
        })
    
    correlation_coefficient = 0.0
    for result in results:
        correlation_coefficient += (result["min_order"] - f(result["n"])) * (result["proof_length"] - sum(r["proof_length"] for r in results) / len(results))
    correlation_coefficient /= math.sqrt(sum((result["min_order"] - f(result["n"])) ** 2 for result in results)) * math.sqrt(sum((result["proof_length"] - sum(r["proof_length"] for r in results) / len(results)) ** 2 for result in results))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": "" if abs(correlation_coefficient) > 0.7 else "correlation_coefficient < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) > 0.7) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")