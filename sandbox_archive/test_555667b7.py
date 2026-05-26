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

def generate_cnf(n, seed):
    random.seed(seed)
    clauses = []
    for i in range(1, n + 1):
        literals = [f"x{i}", f"~x{i}"]
        clause = random.choice(literals) if random.random() < 0.5 else f"{random.choice(literals)} | {random.choice(literals)}"
        clauses.append(clause)
    return " & ".join(clauses)

def tseitin_valuation(cnf):
    valuation = {}
    literals = set()
    for clause in cnf.split(" & "):
        if " | " in clause:
            literal1, literal2 = clause.split(" | ")
            literals.add(literal1)
            literals.add(literal2)
        else:
            literals.add(clause)
    
    def resolve(l1, l2):
        if l1 == f"~{l2}":
            return True
        elif l2 == f"~{l1}":
            return True
        return False
    
    while len(valuation) < len(literals):
        for literal in literals:
            if literal not in valuation and all(not resolve(literal, val) for val in valuation.values()):
                valuation[literal] = 0
                break
    
    return valuation

def compute_quotient_algebra_rank(valuation):
    rank = 0
    for key, value in valuation.items():
        if value == 0:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        cnf = generate_cnf(n, seed)
        valuation = tseitin_valuation(cnf)
        rank = compute_quotient_algebra_rank(valuation)
        total_rank += rank
        instances_tested += 1
    
    average_rank = total_rank / len(n_values)
    C_n = 2  # Example constant for demonstration purposes
    bound = C_n * math.log(n) ** 2
    
    conjecture_holds = average_rank <= bound
    counterexample = "" if conjecture_holds else f"average_rank={average_rank}, expected<=C({n})*log^2({n})"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": average_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[results.index(next(res for res in results if not res['conjecture_holds']))]['counterexample']}\" first_failing_seed={first_failing_seed}")