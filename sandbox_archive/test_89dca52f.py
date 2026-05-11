# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        cnf.append(clause)
    return cnf

def evaluate_cnf(cnf, assignment):
    for clause in cnf:
        if not any([assignment[abs(lit) - 1] == (lit > 0) for lit in clause]):
            return False
    return True

def add_energy(cnf, assignment):
    count = 0
    for x, y, z, w in combinations(range(n), 4):
        if evaluate_cnf(cnf, [assignment[x], assignment[y], assignment[z], assignment[w]]):
            count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = 2 * n
    
    cnf = random_cnf(n, m)
    assignment = [random.choice([0, 1]) for _ in range(n)]
    
    energy = add_energy(cnf, assignment)
    threshold = 0.8 * n**3
    circuit_size = 0.5 * n**2
    
    conjecture_holds = energy < threshold or len(cnf) >= circuit_size
    counterexample = "" if conjecture_holds else f"Energy={energy}, Circuit size={len(cnf)}"
    
    return {
        "metric_name": "Additive Energy",
        "metric_value": energy,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_energy = sum(r["metric_value"] for r in results) / len(results)
    std_energy = (sum((r["metric_value"] - mean_energy)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_energy} std={std_energy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")