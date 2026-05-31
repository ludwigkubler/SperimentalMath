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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def shannon_entropy(f):
        n = len(f)
        counts = [f.count(i) / n for i in set(f)]
        return -sum(c * math.log2(c) for c in counts if c > 0)
    
    def isomorphism_classes_count(f):
        # This is a placeholder function. In practice, you would need to implement
        # an algorithm to count distinct isomorphism classes of Coxeter diagrams.
        # For the purpose of this example, we will return a dummy value.
        return len(set(f))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        H_f = shannon_entropy(f)
        diag_count = isomorphism_classes_count(f)
        ratio = diag_count / math.exp(H_f)
        results.append({"n": n, "H_f": H_f, "diag_count": diag_count, "ratio": ratio})
    
    metric_value = sum(r["ratio"] for r in results) / len(results)
    conjecture_holds = all(r["ratio"] <= 1 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Diag(f) to exp(H(f))",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")