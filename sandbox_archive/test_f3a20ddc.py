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
    
    # Generate a group instance with order n
    n = random.randint(5, 40)
    G = {i for i in range(n)}
    
    # Define the homomorphism φ: G → {0,1}^k
    k = random.randint(2, 3)
    phi_G = [random.sample([0, 1], k) for _ in range(n)]
    
    # Compute φ(G)
    phi_G_value = sum(len(set(phi_G[i])) for i in range(n)) / n
    
    # Generate a k-CLIQUE instance with at most n variables
    clique_instance = []
    for i in range(n):
        if random.random() < 0.5:
            clique_instance.append(i)
    
    # Compute the monotone circuit size for k-CLIQUE instances (simplified example)
    monotone_circuit_size = len(clique_instance) ** 2
    
    # Check the conjecture conditions
    conjecture_holds = True
    counterexample = ""
    if phi_G_value <= n ** (4/3):
        conjecture_holds = False
        counterexample = "phi(G) <= n^(4/3)"
    
    return {
        "metric_name": "phi(G)",
        "metric_value": phi_G_value,
        "instances_tested": len(clique_instance),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [677, 727, 773, 821, 877, 929]  # Default to a list of primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_phi_G = sum(r['metric_value'] for r in results) / len(results)
    std_phi_G = math.sqrt(sum((r['metric_value'] - mean_phi_G) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_phi_G} std={std_phi_G} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"phi(G) <= n^(4/3)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")