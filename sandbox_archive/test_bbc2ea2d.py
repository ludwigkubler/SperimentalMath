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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def adjacency_matrix(clauses, n):
        M = [[0] * n for _ in range(n)]
        for i, (x, y) in enumerate(clauses):
            x -= 1
            y -= 1
            M[x][y] = 1
            M[y][x] = 1
        return M
    
    def monte_carlo_free_entropy(M, n):
        def characteristic_polynomial(M):
            if len(M) == 0:
                return [1]
            if len(M) == 1:
                return [M[0][0], -1]
            det = 0
            for j in range(len(M)):
                M2 = [row[:j] + row[j+1:] for row in M[1:]]
                det += (-1)**j * M[0][j] * determinant(M2)
            return det
        
        def determinant(M):
            if len(M) == 0:
                return 1
            if len(M) == 1:
                return M[0][0]
            det = 0
            for j in range(len(M)):
                M2 = [row[:j] + row[j+1:] for row in M[1:]]
                det += (-1)**j * M[0][j] * determinant(M2)
            return det
        
        def roots(poly):
            if len(poly) == 1:
                return []
            if len(poly) == 2:
                return [(-poly[1]) / poly[0]]
            a, b, c = poly
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                return []
            sqrt_discriminant = math.sqrt(discriminant)
            roots = [(-b + sqrt_discriminant) / (2*a), (-b - sqrt_discriminant) / (2*a)]
            return roots
        
        poly = characteristic_polynomial(M)
        roots_poly = roots(poly)
        free_entropy = sum(math.log(abs(z)) for z in roots_poly if abs(z) > 0) / n
        return free_entropy
    
    n = 40
    M = adjacency_matrix(generate_3cnf(n), n)
    phi_M = monte_carlo_free_entropy(M, n)
    
    return {
        "metric_name": "free_entropy",
        "metric_value": phi_M,
        "instances_tested": 1,
        "conjecture_holds": phi_M >= 0.2 * n,
        "counterexample": "" if phi_M >= 0.2 * n else f"Graph with n={n}, phi(M)={phi_M}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"phi(M) < 0.2n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples_found")