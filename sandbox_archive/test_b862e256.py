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
    n = random.randint(5, 40)
    k = random.randint(3, min(n-1, 6))
    
    # Generate a random k-clique instance
    vertices = list(range(n))
    edges = []
    for i in range(k):
        for j in range(i+1, k):
            edges.append((vertices[i], vertices[j]))
    
    # Construct the simplicial complex
    simplicial_complex = {frozenset(edge): True for edge in edges}
    
    # Compute homology groups (using a simplified version of Smith normal form)
    def smith_normal_form(matrix):
        rows, cols = len(matrix), len(matrix[0])
        while rows > 0 and cols > 0:
            if matrix[rows-1][cols-1] == 0:
                if sum(matrix[r][cols-1] for r in range(rows)) == 0:
                    cols -= 1
                else:
                    for r in range(rows):
                        matrix[r], matrix[r+1] = matrix[r+1], matrix[r]
            elif sum(matrix[r][cols-1] for r in range(rows)) == 0:
                rows -= 1
            else:
                pivot_row = next(r for r in range(rows) if matrix[r][cols-1] != 0)
                matrix[pivot_row], matrix[rows-1] = matrix[rows-1], matrix[pivot_row]
                pivot = matrix[rows-1][cols-1]
                for r in range(rows):
                    if r != rows-1:
                        factor = -matrix[r][cols-1] // pivot
                        for c in range(cols):
                            matrix[r][c] += factor * matrix[rows-1][c]
                rows -= 1
                cols -= 1
        return matrix
    
    # Compute the minimal rank of homology groups
    def compute_homology_rank(simplicial_complex, k):
        if k == 0:
            return 1
        elif k >= len(simplicial_complex):
            return 0
        
        # Build the boundary matrix
        boundary_matrix = []
        for face in simplicial_complex:
            if len(face) == k+1:
                row = [0] * (len(face) - 1)
                for i, vertex in enumerate(sorted(face)):
                    if vertex in simplicial_complex[frozenset(sorted(set(face) - {vertex}))]:
                        row[i] = 1
                boundary_matrix.append(row)
        
        # Compute the Smith normal form of the boundary matrix
        snf = smith_normal_form(boundary_matrix)
        
        # The rank is the number of non-zero entries on the diagonal
        return sum(1 for entry in snf if entry != 0)
    
    homology_rank = compute_homology_rank(simplicial_complex, k)
    
    # Measure communication complexity (simplified version)
    def communication_complexity(n):
        return n * math.log2(n)  # Simplified polynomial bound
    
    comm_complexity = communication_complexity(n)
    
    # Check if the conjecture holds
    conjecture_holds = homology_rank <= comm_complexity
    counterexample = "" if conjecture_holds else f"homology_rank={homology_rank}, comm_complexity={comm_complexity}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")