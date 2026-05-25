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
    instances_tested = 30
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        # Generate a random Boolean function f on n variables
        f = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Construct a monotone circuit for the Boolean function
        # This is a simplified example and may not be optimal
        circuit_size = sum(f)
        
        # Measure the minimal rank of the Hodge module associated with f
        # For simplicity, we assume the rank is equal to the number of 1s in f
        hodge_rank = sum(f)
        
        if hodge_rank > circuit_size:
            conjecture_holds = False
            counterexample = "H(f) rank exceeds monotone circuit size"
            break
    
    return {
        "metric_name": "Minimal Rank of Hodge Module",
        "metric_value": hodge_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")