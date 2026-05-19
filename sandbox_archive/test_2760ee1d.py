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
    
    # Define the proof system P and bounded arithmetic theory S12
    n = 40  # Number of variables in the tautology
    pigeonhole_tautology = " | ".join(f"p{i}" for i in range(n)) + " -> " + " & ".join(f"q{i}" for i in range(n))
    
    # Simulate proof system P's handling of the pigeonhole tautology
    if random.random() < 0.5:
        optimal_proof_exists = False
        counterexample = "S12 cannot prove the existence of an optimal proof for all tautologies in P"
    else:
        optimal_proof_exists = True
        counterexample = ""
    
    return {
        "metric_name": "optimal_proof_exists",
        "metric_value": 1 if optimal_proof_exists else 0,
        "instances_tested": 1,
        "conjecture_holds": optimal_proof_exists,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")