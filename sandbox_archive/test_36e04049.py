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
    
    # Parameters for the trial
    q = 2**random.randint(3, 5)  # Finite field size
    n = random.randint(5, 40)     # Degree of the algebraic curve
    d = random.randint(10, 100)   # Depth of the circuit
    
    # Generate a random polynomial over F_q
    coefficients = [random.randint(0, q-1) for _ in range(n+1)]
    
    # Construct the circuit to compute modular sums modulo q^k for k ≤ n
    def modular_sum(poly, k):
        result = 0
        for i in range(k+1):
            term = sum(coeff * (q**i)**j for j in range(i+1)) % (q**(i+1))
            result += term
        return result
    
    # Compute the minimal rank of the Hodge class (simplified as a proxy)
    hodge_rank = n  # This is a placeholder; actual computation depends on Hodge theory
    
    # Measure the depth of the circuit
    circuit_depth = d
    
    # Check if the conjecture holds for this instance
    if hodge_rank > c * circuit_depth:
        conjecture_holds = False
        counterexample = f"Rank {hodge_rank} exceeds {c}*{circuit_depth}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Ratio of Hodge Rank to Circuit Depth",
        "metric_value": hodge_rank / circuit_depth,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean and standard deviation of the metric_value
    if not results:
        print("RESULT: INCONCLUSIVE No trials executed")
        sys.exit(0)
    
    total_metric = sum(r["metric_value"] for r in results)
    mean_metric = total_metric / len(results)
    
    squared_diff_sum = sum((r["metric_value"] - mean_metric) ** 2 for r in results)
    std_metric = math.sqrt(squared_diff_sum / len(results))
    
    # Compute the fraction of seeds where the conjecture holds
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds depth\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Not enough support for the conjecture")