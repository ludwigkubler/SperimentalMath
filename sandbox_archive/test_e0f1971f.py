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
    
    # Generate a random polynomial CSP instance with n variables
    n = random.randint(5, 40)
    coefficients = [[random.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    constant_term = random.uniform(-1, 1)
    polynomial = [constant_term] + coefficients
    
    # Compute the Newton polytope vertices
    def newton_polytope(polynomial):
        n = len(polynomial)
        if n == 1:
            return [(0,)]
        vertices = []
        for i in range(n):
            for j in range(i+1, n):
                x = Fraction(-polynomial[i][j], polynomial[j][i])
                y = Fraction(-polynomial[j][i], polynomial[i][j])
                if 0 <= x < 1 and 0 <= y < 1:
                    vertices.append((x, y))
        return vertices
    
    vertices = newton_polytope(polynomial)
    vertex_count = len(vertices)
    
    # Compute the minimal SOS rank required for refutation
    def sos_rank(poly):
        n = len(poly)
        A = [[0] * (n+1) for _ in range(n+1)]
        b = [0] * (n+1)
        A[0][0] = 1
        b[0] = poly[0]
        for i in range(1, n):
            A[i][i-1] = A[i-1][i] = -poly[i][i-1]
            A[i][i] = 2 * poly[i][i]
            b[i] = -poly[i][i+1]
        A[n][n] = 1
        b[n] = 0
        
        for i in range(n):
            if A[i][i] == 0:
                return float('inf')
        
        x = [Fraction(b[i], A[i][i]) for i in range(n)]
        rank = sum(1 for xi in x if xi != 0)
        return rank
    
    sos_rank_value = sos_rank(polynomial)
    
    # Check the conjecture
    conjecture_holds = sos_rank_value >= vertex_count
    counterexample = "" if conjecture_holds else f"SOS Rank {sos_rank_value} < Vertex Count {vertex_count}"
    
    return {
        "metric_name": "SOS Rank",
        "metric_value": sos_rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"SOS Rank < Vertex Count\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")