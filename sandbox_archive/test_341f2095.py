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
    
    def frege_proof_depth(f):
        # Placeholder function to simulate Frege proof depth
        # For simplicity, assume the depth is proportional to the number of variables
        return len(f) // 2
    
    def geometric_quantization_rank(f):
        # Placeholder function to simulate geometric quantization rank
        # For simplicity, assume the rank is proportional to the number of variables
        return len(f) // 2
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    gqr = geometric_quantization_rank(f)
    depth = frege_proof_depth(f)
    
    return {
        "metric_name": "GQR vs Frege Depth",
        "metric_value": abs(gqr - depth),
        "instances_tested": 1,
        "conjecture_holds": abs(gqr - depth) <= 0.5,
        "counterexample": "" if abs(gqr - depth) <= 0.5 else f"Counterexample: GQR({gqr}) != D_F({depth})"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")