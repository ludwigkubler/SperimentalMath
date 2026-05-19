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
    
    n = random.randint(5, 30)
    if n > 3:
        return {
            "metric_name": "SOS Rank",
            "metric_value": -1,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Generate random polynomial CSP instance
    variables = [f"x{i}" for i in range(n)]
    equations = []
    for _ in range(10):
        terms = []
        for var in variables:
            exp = random.randint(1, 2)
            if exp > 1:
                terms.append(f"{var}^{exp}")
            else:
                terms.append(var)
        equations.append("+".join(terms) + "=0")
    
    # Compute Newton polytope vertices (simplified example)
    vertices = [(random.randint(-5, 5), random.randint(-5, 5)) for _ in range(n)]
    
    # Compute minimal SOS rank (simplified example)
    sos_rank = n
    
    return {
        "metric_name": "SOS Rank",
        "metric_value": sos_rank,
        "instances_tested": 1,
        "conjecture_holds": sos_rank >= len(vertices),
        "counterexample": "" if sos_rank >= len(vertices) else f"Vertices: {len(vertices)}, SOS Rank: {sos_rank}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"SOS Rank < Vertex Count\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support or counterexamples found")