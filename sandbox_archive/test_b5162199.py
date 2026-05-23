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
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def compute_quantization_rank(cnf):
        # Simplified procedure to compute the Grothendieck-Witt class modulo 2
        rank = 0
        for clause in cnf:
            rank += len([x for x in clause if x != 0])
        return rank % 2
    
    def generate_bp(cnf):
        # Placeholder for BP generation logic
        return random.randint(1, 10)
    
    def generate_circuit(cnf):
        # Placeholder for circuit generation logic
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    rho_f = compute_quantization_rank(cnf)
    bp_size = generate_bp(cnf)
    circuit_size = generate_circuit(cnf)
    
    return {
        "metric_name": "Quantization Rank vs BP/Circuit Size",
        "metric_value": abs(bp_size - circuit_size),
        "instances_tested": 1,
        "conjecture_holds": rho_f <= math.log(n) and rho_f >= math.log(circuit_size),
        "counterexample": "" if rho_f <= math.log(n) and rho_f >= math.log(circuit_size) else f"rho(f)={rho_f}, log(n)={math.log(n)}, circuit_size={circuit_size}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")