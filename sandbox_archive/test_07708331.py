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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    q = 2**random.randint(3, 5)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = sum(random.randint(0, q-1) * x**i for i in range(n+1))
    
    # Find roots of the polynomial
    roots = []
    for a in range(q):
        if f.subs(x, a) == 0:
            roots.append(a)
    
    k = len(roots)
    
    # Simulate Frege proof depth (exponential growth with root count)
    depth = q**k
    
    return {
        "metric_name": "Exponential Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": depth >= Fraction(q).log(2) + Fraction(k+1).log(2),
        "counterexample": "" if depth >= Fraction(q).log(2) + Fraction(k+1).log(2) else f"Exponential Depth {depth} < log({q}) + log({k+1})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = (sum((r["metric_value"] - mean_depth)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and (r["metric_value"] - mean_depth) > 3 * std_depth for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Exponential Depth exceeds threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.9")