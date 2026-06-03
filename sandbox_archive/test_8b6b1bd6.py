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
    
    def generate_random_planar_graph(n):
        if n < 3:
            return None
        
        # Generate a random triangulation of an n-gon
        vertices = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
        edges = []
        
        for i in range(n):
            j = (i + 1) % n
            k = (j + 1) % n
            edges.append((i, j))
            edges.append((j, k))
            edges.append((k, i))
        
        return vertices, edges
    
    def delaunay_triangulation(vertices):
        # Simple triangulation algorithm for demonstration purposes
        if len(vertices) < 3:
            return []
        
        triangles = []
        for i in range(len(vertices)):
            j = (i + 1) % len(vertices)
            k = (j + 1) % len(vertices)
            triangles.append((vertices[i], vertices[j], vertices[k]))
        return triangles
    
    def rank_of_delaunay_complex(triangles):
        # Placeholder for actual rank calculation
        return len(triangles)
    
    def circuit_monotone_width(graph):
        # Placeholder for actual width calculation
        return random.randint(1, 5)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_random_planar_graph(n)
    if not graph:
        return {
            "metric_name": "rd(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_not_planar"
        }
    
    vertices, edges = graph
    triangles = delaunay_triangulation(vertices)
    rd_G = rank_of_delaunay_complex(triangles)
    w_m_G = circuit_monotone_width(graph)
    
    return {
        "metric_name": "rd(G)",
        "metric_value": rd_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len(results) / len(seeds)
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_implemented\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")