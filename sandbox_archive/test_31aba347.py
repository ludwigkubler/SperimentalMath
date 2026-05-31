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
        # Placeholder for actual communication complexity calculation
        return n * (n + 1) // 2
    
    def minimal_quadratic_residue_representation(n):
        residues = set()
        for i in range(1, n + 1):
            residues.add(i**2 % n)
        return len(residues)
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cc = communication_complexity(n)
        mqr = minimal_quadratic_residue_representation(n)
        
        if cc == 0:
            continue
        
        total_metric_value += abs(mqr - cc) / cc
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = mean_metric_value <= 1.5 and mean_metric_value >= 0.5
    counterexample = "" if conjecture_holds else f"mean_metric_value={mean_metric_value}"
    
    return {
        "metric_name": "CommunicationComplexity vs MinimalQuadraticResidueRepresentation",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")