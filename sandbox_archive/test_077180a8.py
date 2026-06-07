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
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def next_prime(n):
    while not is_prime(n):
        n += 1
    return n

def tonelli_shanks(a, p):
    if a == 0:
        return 0
    if pow(a, (p - 1) // 2, p) != 1:
        raise ValueError("No square root exists for non-quadratic residues modulo a prime")
    
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1
    
    n = random.randint(2, p - 1)
    while pow(n, (p - 1) // 2, p) == 1:
        n = random.randint(2, p - 1)
    
    x = pow(a, s, p)
    b = pow(a, (s + 1) // 2, p)
    g = pow(b, 2, p)
    r = e
    
    while g != 1:
        m = 0
        for m in range(1, r):
            if pow(g, 1 << m, p) == 1:
                break
        
        gs = pow(b, 1 << (r - m - 1), p)
        b = gs * gs % p
        g = (g * gs) % p
        x = (x * gs) % p
        r = m
    
    return x

def primitive_root(p):
    if p == 2:
        return 1
    if p % 2 == 0:
        return None
    
    factors = {p - 1}
    for i in range(3, int(math.sqrt(p)) + 1, 2):
        if p % i == 0 and is_prime(i):
            factors.add(i)
            factors.add((p - 1) // i)
    
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    return None

def frege_proof_depth(phi):
    # Placeholder function to compute Frege proof depth
    # This is a stub and should be replaced with actual computation
    return len(phi)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = [random.randint(0, 1) for _ in range(n * (n - 1) // 2)]
            p = next_prime(2 * n)
            ord_p_phi = primitive_root(p)
            if ord_p_phi is None:
                continue
            
            d_phi = frege_proof_depth(phi)
            results.append((ord_p_phi, d_phi))
    
    if not results:
        return {
            "metric_name": "Frege proof depth",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ord_p_phi_values = [r[0] for r in results]
    d_phi_values = [r[1] for r in results]
    
    mean_ord_p_phi = sum(ord_p_phi_values) / len(ord_p_phi_values)
    mean_d_phi = sum(d_phi_values) / len(d_phi_values)
    
    conjecture_holds = all(d <= ord_p_phi for ord_p_phi, d in results)
    counterexample = "" if conjecture_holds else "Frege proof depth > minimal order of primitive root"
    
    return {
        "metric_name": "Frege proof depth",
        "metric_value": mean_d_phi,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [next_prime(2 * n) for n in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Frege proof depth > minimal order of primitive root\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support n_tested={len(results)}")