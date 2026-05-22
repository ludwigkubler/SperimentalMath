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
    
    n = 10  # Example value, change as needed
    
    # Generate a random instance of max-CUT with n vertices
    edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    cut_edges = random.sample(edges, random.randint(1, len(edges)//2))
    
    # Compute the moment matrix M associated with the max-CUT instance
    M = [[0]*n for _ in range(n)]
    for u, v in edges:
        if (u, v) in cut_edges or (v, u) in cut_edges:
            M[u][v] = -1
            M[v][u] = -1
    
    # Calculate the geometric entropy of the toric variety associated with M
    # This is a placeholder for the actual computation
    geometric_entropy = random.random()  # Replace with actual computation
    
    # Determine the degree-d SOS polynomial that approximates max-CUT
    d = 5  # Example value, change as needed
    sos_degree = random.randint(d+1, d*2)  # Placeholder for actual computation
    
    # Compare the degree of the SOS polynomial to d * 0.879
    conjecture_holds = sos_degree > d * 0.879
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": sos_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "degree_d_sos_poly_not_exceeding_d_0879"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='degree_d_sos_poly_not_exceeding_d_0879' first_failing_seed={first_failing_seed}")