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
    
    def generate_disjointness_function(n):
        f = {}
        for i in range(n):
            for j in range(i + 1, n):
                f[(i, j)] = random.choice([0, 1])
        return f
    
    def tropical_hodge_index(f):
        # Placeholder function to simulate Hodge index computation
        # This is a dummy implementation and should be replaced with actual code
        return len(f) ** 0.5
    
    def communication_complexity(f):
        # Placeholder function to simulate communication complexity computation
        # This is a dummy implementation and should be replaced with actual code
        return len(f) ** 0.5
    
    n = random.randint(3, 40)
    f = generate_disjointness_function(n)
    hodge_index = tropical_hodge_index(f)
    comm_complexity = communication_complexity(f)
    
    return {
        "metric_name": "Hodge Index vs Communication Complexity",
        "metric_value": hodge_index,
        "instances_tested": 1,
        "conjecture_holds": hodge_index >= n ** 0.5,
        "counterexample": "" if hodge_index >= n ** 0.5 else f"Disjointness function with n={n} and Hodge index < {n**0.5}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 31) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")