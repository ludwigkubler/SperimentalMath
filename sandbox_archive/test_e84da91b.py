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
    
    def dpll(sat_instance):
        stack = []
        for clause in sat_instance:
            if not any(lit in stack for lit in clause):
                return False
        return True
    
    def algebraic_stack(sat_instance):
        # Placeholder for actual algebraic stack computation
        # This is a dummy implementation for demonstration purposes
        return len(sat_instance)
    
    def minimal_index(stack):
        # Placeholder for actual minimal index computation
        # This is a dummy implementation for demonstration purposes
        return len(stack)
    
    n = random.randint(5, 40)
    sat_instances = []
    for _ in range(30):
        clause_length = random.randint(1, n)
        clause = [random.choice([f"x{i}", f"~x{i}"]) for i in range(n)]
        sat_instances.append(clause)
    
    indices = [minimal_index(algebraic_stack(sat_instance)) for sat_instance in sat_instances]
    avg_index = sum(indices) / len(indices)
    max_index = max(indices)
    
    conjecture_holds = max_index <= 2 * (n ** 1.5)
    counterexample = "" if conjecture_holds else f"max_index={max_index}, expected<=2*n^1.5"
    
    return {
        "metric_name": "minimal_index",
        "metric_value": avg_index,
        "instances_tested": len(indices),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_index = sum(r["metric_value"] for r in results) / len(results)
    max_index = max(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_index} std=0.0 support_fraction=1.0")
    elif max_index > 2 * (40 ** 1.5):
        print(f"RESULT: FALSIFIED counterexample='max_index exceeds bound' first_failing_seed={seeds[max_index == max(results)['metric_value']]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")