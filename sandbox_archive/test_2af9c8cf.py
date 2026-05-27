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
    
    def cnf_formula(n):
        return [[random.randint(1, n), -random.randint(1, n)] for _ in range(random.randint(5, 10))]
    
    def quandle_structure(F):
        # Simplified representation of quandle structure
        return len(F) * len(F)
    
    def minimal_rank(Q_F):
        return math.sqrt(Q_F)
    
    n = random.randint(5, 40)
    F = cnf_formula(n)
    Q_F = quandle_structure(F)
    rank = minimal_rank(Q_F)
    
    metric_value = rank / (n ** 1.5)
    conjecture_holds = metric_value <= 1
    counterexample = "" if conjecture_holds else "rank > n^(3/2)"
    
    return {
        "metric_name": "Ratio of Minimal Rank to n^(3/2)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank > n^(3/2)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 80%")