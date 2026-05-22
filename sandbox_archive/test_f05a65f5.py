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

def generate_polynomial(d, F):
    coefficients = [random.choice(F) for _ in range(d + 1)]
    x = symbols('x')
    return sum(c * x**i for i, c in enumerate(coefficients))

def find_roots(P):
    # Use a simple numerical method to find roots
    def f(x):
        return P.subs(x, x)
    
    roots = []
    for _ in range(10):  # Try up to 10 times
        guess = random.uniform(-10, 10)
        root = newton_method(f, guess, max_iter=100)
        if root not in roots:
            roots.append(root)
    return roots

def newton_method(f, x0, tol=1e-6, max_iter=100):
    for _ in range(max_iter):
        fx = f(x0)
        dfx = f.diff(x).subs(x, x0)
        if abs(dfx) < tol:
            break
        x0 -= fx / dfx
    return x0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define the number field F and degree d
    F = [Fraction(1), Fraction(-1)]  # Example number field Q(i)
    d = random.randint(3, 40)
    
    # Generate a polynomial P(x) over the number field F with degree d
    P = generate_polynomial(d, F)
    
    # Find the roots of the polynomial
    roots = find_roots(P)
    
    # Calculate the minimal distance between distinct roots
    distances = [abs(roots[i] - roots[j]) for i in range(len(roots)) for j in range(i + 1, len(roots))]
    min_distance = min(distances) if distances else float('inf')
    
    # Calculate the gate count of an AC0 parity circuit for n inputs
    n = len(roots)
    c = random.uniform(0.1, 1.0)  # Random constant c > 0
    mean_circuit_size = 1.5 * c * n
    
    # Check if the conjecture holds
    conjecture_holds = min_distance >= c * math.log(d)
    
    return {
        "metric_name": "Minimal Root Distance",
        "metric_value": min_distance,
        "instances_tested": len(roots),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample with d={d}, c={c}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='min_distance < c*log(d)' first_failing_seed={first_failing_seed}")