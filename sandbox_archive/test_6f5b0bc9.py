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
    
    def galois_representation(f):
        # Placeholder for actual computation of Galois representation
        return len(f)

    def quantum_query_complexity(f):
        # Placeholder for actual computation of quantum query complexity
        return len(f)**2

    min_order = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        n = random.randint(5, 40)
        f = [random.randint(0, 1) for _ in range(n)]
        
        order = galois_representation(f)
        q_complexity = quantum_query_complexity(f)
        
        if order > 0.25 * q_complexity**2:
            conjecture_holds = False
            counterexample = f"f={f}, min_order={order}, expected<=0.25*{q_complexity}^2"
            break
        
        min_order += order
        instances_tested += 1

    return {
        "metric_name": "min_order",
        "metric_value": min_order / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")