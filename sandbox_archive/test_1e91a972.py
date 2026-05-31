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
    
    def communication_complexity(n):
        return n * (n - 1) // 2
    
    def minimal_quadratic_residue_representation(n):
        residues = set()
        for i in range(1, n + 1):
            residues.add(i**2 % n)
        return len(residues)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cc = communication_complexity(n)
        mqr = minimal_quadratic_residue_representation(n)
        results.append((cc, mqr))
    
    if len(results) < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([n for _, n in results]),
            "conjecture_holds": False,
            "counterexample": "Too few instances"
        }
    
    cc_values = [cc for cc, _ in results]
    mqr_values = [mqr for _, mqr in results]
    
    mean_cc = sum(cc_values) / len(cc_values)
    mean_mqr = sum(mqr_values) / len(mqr_values)
    
    if abs(mean_mqr - mean_cc) > 0.5 * mean_cc:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([n for _, n in results]),
            "conjecture_holds": False,
            "counterexample": "Non-linear correlation"
        }
    
    return {
        "metric_name": "Correlation",
        "metric_value": mean_mqr / mean_cc,
        "instances_tested": len(results),
        "n_max": max([n for _, n in results]),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                                              31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 
                                              73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-linear correlation\" first_failing_seed={first_failing_seed}")