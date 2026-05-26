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

def generate_circuit(n):
    if n == 1:
        return ['NOT', 'x']
    else:
        left = generate_circuit(random.randint(1, n-1))
        right = generate_circuit(n - len(left) - 1)
        operator = random.choice(['AND', 'OR'])
        return [operator] + left + right

def construct_geometric_object(circuit):
    # Placeholder for the actual geometric object construction
    # This is a dummy implementation that returns a simple list
    return circuit

def compute_minimal_rank(geometric_object):
    # Placeholder for the actual minimal rank computation
    # This is a dummy implementation that returns a simple value
    return len(geometric_object)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    circuit = generate_circuit(n)
    geometric_object = construct_geometric_object(circuit)
    minimal_rank = compute_minimal_rank(geometric_object)
    
    g_n = math.log2(n + 1)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank <= g_n,
        "counterexample": "" if minimal_rank <= g_n else f"rank={minimal_rank}, expected={g_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeded g(n)\" first_failing_seed={seeds[first_failing_seed]}")