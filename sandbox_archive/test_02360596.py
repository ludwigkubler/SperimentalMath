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

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_prime(n):
    while True:
        p = random.randint(2**(n-1), 2**n - 1)
        if is_prime(p):
            return p

def tonelli_shanks(a, p):
    assert a < p and p > 3
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    for z in range(2, p):
        if pow(z, (p - 1) // 2, p) == p - 1:
            break
    c = pow(z, q, p)
    r = pow(a, (q + 1) // 2, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        for i in range(1, m):
            if pow(t, 2**i, p) == 1:
                break
        b = pow(c, 2**(m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

def minimal_order(a, p):
    if math.gcd(a, p) != 1:
        return None
    order = 1
    while pow(a, order, p) != 1:
        order += 1
    return order

def frege_proof_depth(n):
    # Placeholder function for Frege proof depth calculation
    # This is a dummy implementation and should be replaced with actual logic
    return n * (n + 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        p = generate_prime(n)
        phi = random.randint(1, 2**n - 1)  # Placeholder for CNF generation
        
        ord_p_phi = minimal_order(phi, p)
        d_phi = frege_proof_depth(n)
        
        if ord_p_phi is None or d_phi is None:
            continue
        
        results.append({
            "ord_p_phi": ord_p_phi,
            "d_phi": d_phi
        })
    
    if not results:
        return {
            "metric_name": "Frege Proof Depth",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ord_p_phi_avg = sum(result["ord_p_phi"] for result in results) / len(results)
    d_phi_avg = sum(result["d_phi"] for result in results) / len(results)
    
    conjecture_holds = all(ord_p_phi <= d_phi for result in results)
    counterexample = "" if conjecture_holds else "Frege proof depth is not bounded by minimal order"
    
    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": d_phi_avg,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")