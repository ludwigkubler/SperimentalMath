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
    
    # Define constants and parameters
    n = 30  # Input size
    depth = random.randint(5, 40)  # Depth of ACC⁰ circuit
    num_trials = 100  # Number of instances to test
    
    total_edges = 0
    
    for _ in range(num_trials):
        # Generate a random polynomial f(x1, ..., xn)
        coefficients = [random.randint(0, 1) for _ in range(n)]
        f = sum(c * x**i for i, c in enumerate(coefficients))
        
        # Construct the incidence graph G_f
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if f.subs({x: i}) == f.subs({x: j}):
                    edges.add((i, j))
        
        total_edges += len(edges)
    
    avg_edges_per_trial = Fraction(total_edges, num_trials)
    metric_value = avg_edges_per_trial / math.sqrt(n * depth)
    
    # Define the acceptance criterion
    beta = 1.0  # Example constant
    T = 0.1  # Example threshold
    
    conjecture_holds = metric_value <= beta + T and metric_value <= 10
    counterexample = "" if conjecture_holds else "beta_threshold_exceeded"
    
    return {
        "metric_name": "avg_edges_per_trial",
        "metric_value": avg_edges_per_trial,
        "instances_tested": num_trials,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"beta_threshold_exceeded\" first_failing_seed={first_failing_seed}")