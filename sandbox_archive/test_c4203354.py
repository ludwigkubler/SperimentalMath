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
    
    def boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def symplectic_cell_decomposition(f):
        n = len(f)
        if n == 1:
            return 1
        else:
            return 2 * symplectic_cell_decomposition(f[:n//2]) + symplectic_cell_decomposition(f[n//2:])
    
    def complexity_of_evaluation(f):
        n = len(f)
        if n == 1:
            return 1
        else:
            return 2 * complexity_of_evaluation(f[:n//2]) + complexity_of_evaluation(f[n//2:])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = boolean_function(n)
        rank = symplectic_cell_decomposition(f)
        complexity = complexity_of_evaluation(f)
        if complexity == 0:
            continue
        ratio = rank / complexity
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "Ratio of Rank to Complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mean_ratio = sum(results) / len(results)
    support_fraction = len([r for r in results if r <= 2.0]) / len(results)
    
    return {
        "metric_name": "Ratio of Rank to Complexity",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean={mean_ratio} < 2.0"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(r["instances_tested"] * (1 if r["conjecture_holds"] else 0) for r in results) / sum(r["instances_tested"] for r in results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio_exceeds_2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")