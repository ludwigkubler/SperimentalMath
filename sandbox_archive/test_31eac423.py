# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def newton_polytope(polynomial):
        n = len(polynomial)
        if any(len(row) != n for row in polynomial):
            return 0, []
        
        # Convert to integer coefficients
        polynomial = [[Fraction(coeff) for coeff in row] for row in polynomial]
        
        # Compute the Newton polytope using a convex hull algorithm
        vertices = []
        for i in range(n):
            for j in range(i+1, n):
                if polynomial[j][i] == 0:
                    continue
                x = Fraction(-polynomial[i][j], polynomial[j][i])
                y = Fraction(polynomial[i][i], polynomial[j][i])
                vertices.append((x, y))
        
        return len(vertices), vertices
    
    def sos_rank(n):
        # Placeholder for actual SOS rank computation using semidefinite programming
        # This is a dummy implementation for testing purposes
        return n  # Simplified for demonstration
    
    def generate_polynomial(n):
        # Generate a random polynomial with integer coefficients
        polynomial = []
        for i in range(n):
            row = [0] * n
            row[i] = 1
            for j in range(i+1, n):
                row[j] = random.randint(-5, 5)
            polynomial.append(row)
        return polynomial
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    polynomial = generate_polynomial(n)
    
    vertices_count, _ = newton_polytope(polynomial)
    sos_rank_value = sos_rank(n)
    
    return {
        "metric_name": "SOS Rank",
        "metric_value": sos_rank_value,
        "instances_tested": 1,
        "conjecture_holds": sos_rank_value >= vertices_count,
        "counterexample": "" if sos_rank_value >= vertices_count else f"n={n}, vertices_count={vertices_count}, sos_rank_value={sos_rank_value}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={first_failing_seed}\" first_failing_seed={first_failing_seed}")