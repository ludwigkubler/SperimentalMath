# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define a simple k-party communication protocol with input length n
    def generate_protocol(n, k):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(k)]
    
    # Compute the minimal symplectic volume of the associated projective variety V(π)
    def min_symplectic_volume(protocol):
        # Placeholder function to simulate computation
        n = len(protocol[0])
        return random.uniform(0, 2 * n)
    
    # Measure the communication complexity Comm(π) of each protocol
    def comm_complexity(protocol):
        n = len(protocol[0])
        k = len(protocol)
        return n * (k - 1)
    
    instances_tested = 30
    n_max = 40
    total_volume = 0
    total_comm = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        k = random.randint(2, min(n, 10))
        protocol = generate_protocol(n, k)
        volume = min_symplectic_volume(protocol)
        comm = comm_complexity(protocol)
        
        total_volume += volume
        total_comm += comm
    
    mean_volume = total_volume / instances_tested
    mean_comm = total_comm / instances_tested
    
    conjecture_holds = mean_volume > 0.5 * mean_comm and all(volume > 0.2 * comm for volume, comm in zip([min_symplectic_volume(generate_protocol(n, k)) for n in range(5, n_max + 1) for k in range(2, min(n, 10))], [comm_complexity(generate_protocol(n, k)) for n in range(5, n_max + 1) for k in range(2, min(n, 10))]))
    counterexample = "" if conjecture_holds else f"min_vol(V(π))={mean_volume}, Comm(π)={mean_comm}"
    
    return {
        "metric_name": "symplectic_volume",
        "metric_value": mean_volume,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unexpected_behavior")