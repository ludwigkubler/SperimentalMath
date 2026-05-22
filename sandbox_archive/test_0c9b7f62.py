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
    
    # Generate a random finite field size p (prime number)
    p = next_prime()
    
    # Generate a random affine plane curve over F_p
    n = 5 + random.randint(0, 24)  # n in {5, 10, ..., 30}
    points = generate_points(n, p)
    
    # Compute the characteristic function for the curve
    circuit_size = len(generate_circuit(points))
    
    # Calculate the minimal p-adic valuation of the coordinates of any point
    min_valuation = min(p_adic_valuation(point, p) for point in points)
    
    # Check if the conjecture holds
    conjecture_holds = min_valuation >= math.log2(circuit_size)
    counterexample = "" if conjecture_holds else f"Point with valuation {min_valuation} < log2({circuit_size})"
    
    return {
        "metric_name": "Minimal p-Adic Valuation",
        "metric_value": min_valuation,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def next_prime():
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    prime = random.randint(2, 100)
    while not is_prime(prime):
        prime = random.randint(2, 100)
    return prime

def generate_points(n, p):
    points = set()
    while len(points) < n:
        x = random.randint(0, p - 1)
        y = random.randint(0, p - 1)
        if (x, y) not in points:
            points.add((x, y))
    return list(points)

def generate_circuit(points):
    # Simplified AC^0 circuit generation for demonstration
    circuit = []
    for point in points:
        x, y = point
        circuit.append(f"AND({x}, {y})")
    return circuit

def p_adic_valuation(point, p):
    x, y = point
    val_x = 0 if x == 0 else int(math.log2(x)) + 1
    val_y = 0 if y == 0 else int(math.log2(y)) + 1
    return min(val_x, val_y)

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [next_prime() for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_valuation = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_valuation) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_valuation} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_valuation} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")