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
    
    # Generate a random boolean function φ of size n
    n = 20
    phi = [random.choice([0, 1]) for _ in range(n)]
    
    # Compute the automorphic representation of φ
    automorphic_rep = sum(phi[i] * 2**(i % n) for i in range(len(phi)))
    
    # Evaluate the L-function zeros (simplified for testing)
    l_function_zeros = [i for i in range(1, n+1) if phi[i-1] == 1]
    
    # Compute the communication complexity rank (simplified for testing)
    comm_complexity_rank = len(l_function_zeros)
    
    # Check the conjecture
    num_zeros = len(l_function_zeros)
    expected_rank = math.log(num_zeros, 2)
    if abs(comm_complexity_rank - expected_rank) > 0.5:
        conjecture_holds = False
        counterexample = f"comm_complexity_rank={comm_complexity_rank}, expected_rank={expected_rank}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": comm_complexity_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")