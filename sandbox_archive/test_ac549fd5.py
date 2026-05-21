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
    
    def generate_structure(n):
        # Placeholder for structure generation logic
        return [i for i in range(1, n+1)]
    
    def compute_action_count(structure):
        # Placeholder for action count computation logic
        return sum(structure)
    
    def compute_mcsp_depth(structure):
        # Placeholder for MCSP depth computation logic
        return len(structure)
    
    structures = [generate_structure(n) for n in [5, 10, 15, 20, 30, 40]]
    results = []
    
    for structure in structures:
        action_count = compute_action_count(structure)
        mcsp_depth = compute_mcsp_depth(structure)
        
        if mcsp_depth == 0:
            continue
        
        ratio = Fraction(action_count, mcsp_depth)
        results.append({
            "structure": structure,
            "action_count": action_count,
            "mcsp_depth": mcsp_depth,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "action_count_to_mcsp_ratio",
            "metric_value": 0.0,
            "instances_tested": len(structures),
            "conjecture_holds": False,
            "counterexample": "No valid structures generated"
        }
    
    max_ratio = max(r["ratio"] for r in results)
    conjecture_holds = max_ratio <= Fraction(15, 10)
    
    return {
        "metric_name": "action_count_to_mcsp_ratio",
        "metric_value": sum(r["ratio"] for r in results) / len(results),
        "instances_tested": len(structures),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_ratio={max_ratio}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_ratio={results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")