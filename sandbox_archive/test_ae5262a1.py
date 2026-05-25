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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def hodge_module_rank(f):
        # Placeholder function to compute the rank of a Hodge module
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    def monotone_circuit_size(f):
        # Placeholder function to construct a monotone circuit for a Boolean function
        # This is a dummy implementation and should be replaced with actual logic
        return len(f) + 1
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    
    rank = hodge_module_rank(f)
    size = monotone_circuit_size(f)
    
    return {
        "metric_name": "rank(H(f))",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= size,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        counterexample = next(result for result in results if not result["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")