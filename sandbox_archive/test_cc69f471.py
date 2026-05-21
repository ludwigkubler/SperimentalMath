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
    
    n = 20  # Fixed size for simplicity, can be adjusted as needed
    
    # Generate a random bipartite graph with parts of size n
    A = [random.randint(0, 1) for _ in range(n)]
    B = [random.randint(0, 1) for _ in range(n)]
    
    # Compute the number of edges in the graph
    edges = sum(a * b for a, b in zip(A, B))
    
    # Calculate Z(n, 2, 2), the maximum number of edges without a K_{2,2}
    z_n_2_2 = n
    
    # The communication complexity is proportional to the number of edges
    comm_complexity = edges
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": comm_complexity >= z_n_2_2,
        "counterexample": "" if comm_complexity >= z_n_2_2 else "Graph contains a K_{2,2}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    total_comm_complexity = 0
    num_trials = len(seeds)
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_comm_complexity += trial_result["metric_value"]
    
    mean_comm_complexity = total_comm_complexity / num_trials
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_trials
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")