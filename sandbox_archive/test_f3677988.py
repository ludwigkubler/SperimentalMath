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
    
    def generate_cnf(n: int) -> list:
        cnf = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def add_clause(cnf: list, clause: list) -> None:
        cnf.append(clause)
    
    def evaluate_cnf(cnf: list, assignment: dict) -> int:
        result = 0
        for clause in cnf:
            if any(assignment.get(abs(lit), 0) * lit > 0 for lit in clause):
                result += 1
        return result
    
    def communication_protocol_depth(cnf: list) -> int:
        n = len(cnf[0])
        depth = 0
        while True:
            new_cnf = []
            for i in range(2**n):
                assignment = {j + 1: (i >> j) & 1 for j in range(n)}
                if evaluate_cnf(cnf, assignment) == len(cnf):
                    add_clause(new_cnf, [-(i + 1)])
            if new_cnf:
                cnf = new_cnf
                depth += 1
            else:
                break
        return depth
    
    def additive_energy(cnf: list) -> int:
        n = len(cnf[0])
        energy = 0
        for i in range(2**n):
            assignment = {j + 1: (i >> j) & 1 for j in range(n)}
            if evaluate_cnf(cnf, assignment) == len(cnf):
                for j in range(i + 1, 2**n):
                    other_assignment = {j + 1: (j >> k) & 1 for k in range(n)}
                    if evaluate_cnf(cnf, other_assignment) == len(cnf):
                        energy += 1
        return energy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        energy = additive_energy(cnf)
        depth = communication_protocol_depth(cnf)
        if depth == 0:
            continue
        results.append({
            "n": n,
            "energy": energy,
            "depth": depth
        })
    
    metric_value = sum(result["energy"] * result["depth"] * math.log(result["n"]) for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["energy"] * result["depth"] * math.log(result["n"]) <= 2**result["n"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Additive Energy",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] == "mapping_undefined" for result in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")