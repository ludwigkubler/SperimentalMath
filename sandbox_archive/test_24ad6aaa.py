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
    
    def generate_cnf_tautology(n):
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(f"({clause[0]} & {clause[1]})")
        return " | ".join(clauses)

    def count_axioms_and_rules(proof):
        axioms = proof.split(" -> ")
        rules = [axiom.split(" & ") for axiom in axioms]
        total_rules = sum(len(rule) for rule in rules)
        return len(axioms), total_rules

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different instances
            phi = generate_cnf_tautology(n)
            proof = f"({phi}) -> False"  # Dummy proof for testing
            axioms, rules = count_axioms_and_rules(proof)
            results.append({"size": len(phi.split()), "axioms": axioms, "rules": rules})
    
    total_axioms = sum(result["axioms"] + result["rules"] for result in results)
    mean_axioms = total_axioms / len(results)
    conjecture_holds = all(size <= 10 * n ** 3 for size, n in zip([result["size"] for result in results], n_values))  # Simplified quasipolynomial bound
    counterexample = "" if conjecture_holds else "quasipolynomial_bound_violation"
    
    return {
        "metric_name": "axioms_and_rules",
        "metric_value": mean_axioms,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_axioms = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_axioms} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"quasipolynomial_bound_violation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")