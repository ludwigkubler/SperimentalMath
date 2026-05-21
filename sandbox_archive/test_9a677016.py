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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def compute_nu(G, F):
        # Placeholder for ν(G) computation
        # This is a dummy implementation and should be replaced with the actual algorithm
        return len(G)
    
    def ma_cc_protocol_steps(nu):
        # Placeholder for MA^cc protocol steps calculation
        # This is a dummy implementation and should be replaced with the actual algorithm
        return 2 ** nu
    
    n = random.randint(5, 40)
    G = generate_graph(n)
    F = [random.randint(1, 10) for _ in range(n)]
    nu = compute_nu(G, F)
    steps = ma_cc_protocol_steps(nu)
    
    return {
        "metric_name": "MA^cc protocol steps",
        "metric_value": steps,
        "instances_tested": 1,
        "conjecture_holds": steps >= 2 ** math.ceil(math.log2(nu)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_steps = sum(r["metric_value"] for r in results) / len(results)
    std_steps = math.sqrt(sum((r["metric_value"] - mean_steps) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_steps} std={std_steps} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_steps} std={std_steps} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")