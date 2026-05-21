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
    
    def generate_random_polyhedron(n):
        # Generate a random polyhedron with n vertices
        vertices = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
        facets = []
        for i in range(n):
            facet = [vertices[j] for j in range(i+1, n) if (i, j) not in facets]
            facets.append(facet)
        return vertices, facets

    def distance(point, line):
        # Calculate the perpendicular distance from a point to a line
        x0, y0 = point
        x1, y1 = line[0]
        x2, y2 = line[1]
        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        return numerator / denominator

    def min_geometric_invariant(vertices, facets):
        # Find the minimum geometric invariant of a hyperplane section
        min_dist = float('inf')
        for facet in facets:
            line = random.sample(facet, 2)
            for vertex in vertices:
                dist = distance(vertex, line)
                if dist < min_dist:
                    min_dist = dist
        return min_dist

    def communication_complexity(n):
        # Calculate the communication complexity of a function f
        return math.log2(n)**2

    n = random.randint(5, 40)  # Number of vertices in the polyhedron
    vertices, facets = generate_random_polyhedron(n)
    min_dist = min_geometric_invariant(vertices, facets)
    comm_complexity = communication_complexity(n)

    return {
        "metric_name": "min_geometric_invariant",
        "metric_value": min_dist,
        "instances_tested": 1,
        "conjecture_holds": min_dist >= n * math.log2(n),
        "counterexample": "" if min_dist >= n * math.log2(n) else f"n={n}, min_dist={min_dist}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")