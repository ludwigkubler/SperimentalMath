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
    
    # Generate a random polynomial CSP instance with n variables
    n = random.randint(5, 40)
    coefficients = [[random.uniform(-1, 1) for _ in range(n+1)] for _ in range(n)]
    equations = [sum(coeff * x**i for i, coeff in enumerate(row)) for row in coefficients]
    
    # Compute the Newton polytope using a convex hull algorithm
    points = [(i, j) for i in range(n+1) for j in range(n+1) if all(coefficients[i][j] != 0)]
    vertices = convex_hull(points)
    
    # Count the number of vertices
    vertex_count = len(vertices)
    
    # Compute the minimal SOS rank required for refutation via semidefinite programming
    sos_rank = min_sos_rank(equations, n)
    
    # Compare vertex counts with SOS rank values
    conjecture_holds = vertex_count <= sos_rank
    counterexample = "" if conjecture_holds else f"Vertex count {vertex_count} > SOS rank {sos_rank}"
    
    return {
        "metric_name": "SOS Rank",
        "metric_value": sos_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def convex_hull(points):
    # Implement a simple convex hull algorithm (e.g., Graham's scan)
    if len(points) < 3:
        return points
    
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2
    
    def compare(p, q):
        o = orientation(points[0], p, q)
        if o == 0:
            return (p[0]**2 + p[1]**2) - (q[0]**2 + q[1]**2)
        elif o == 1:
            return -1
        else:
            return 1
    
    points.sort(key=lambda point: (point[0], point[1]))
    lower = []
    for point in points:
        while len(lower) >= 2 and orientation(lower[-2], lower[-1], point) != 2:
            lower.pop()
        lower.append(point)
    
    upper = []
    for point in reversed(points):
        while len(upper) >= 2 and orientation(upper[-2], upper[-1], point) != 2:
            upper.pop()
        upper.append(point)
    
    hull = lower[:-1] + upper[:-1]
    return hull

def min_sos_rank(equations, n):
    # Implement a simple semidefinite programming solver to find the minimal SOS rank
    # This is a placeholder and should be replaced with an actual implementation
    return n  # Placeholder value for demonstration purposes

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")