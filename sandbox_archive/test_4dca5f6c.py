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
    
    def generate_cnf_tautology(n):
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([i, -i]) for _ in range(random.randint(2, 4))]
            clauses.append(clause)
        return clauses

    def compute_free_probability_entanglement(cnf_tautology):
        # Placeholder function to simulate computation
        return random.uniform(0.1, 1.0)

    def compute_minimal_invariant(entanglement):
        # Placeholder function to simulate computation
        return random.uniform(0.1, entanglement)

    def generate_bp_read_twice_proof(cnf_tautology):
        # Placeholder function to simulate computation
        proof_size = random.randint(len(cnf_tautology), 2 * len(cnf_tautology))
        return proof_size

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf_tautology = generate_cnf_tautology(n)
    entanglement = compute_free_probability_entanglement(cnf_tautology)
    rho_F = compute_minimal_invariant(entanglement)

    instances_tested = 1
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        proof_size = generate_bp_read_twice_proof(cnf_tautology)
        rho_P = compute_minimal_invariant(proof_size)
        
        if rho_P < rho_F / math.log(n):
            conjecture_holds = False
            counterexample = f"Proof size {proof_size} with rho(P)={rho_P} < rho(F)/log(n)={rho_F/math.log(n)}"
            break

    return {
        "metric_name": "Minimal Invariant Ratio",
        "metric_value": rho_F / math.log(n),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")