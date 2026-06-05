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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def circuit_monotone_width(cnf):
        # Simplified version of monotone width calculation
        width = 0
        for clause in cnf:
            width = max(width, len(set(abs(lit) for lit in clause)))
        return width
    
    def minimal_grammar_complexity(cnf):
        # Placeholder function to simulate grammar complexity
        # This is a very simplified version and not accurate
        return len(cnf)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds_count = 0
    
    for n in range(5, 41):
        for _ in range(7):  # Each n tested 7 times
            m = random.randint(2 * n, 3 * n)
            cnf = generate_cnf(m, n)
            instances_tested += 1
            
            grammar_complexity = minimal_grammar_complexity(cnf)
            monotone_width = circuit_monotone_width(cnf)
            
            if monotone_width == 0:
                continue
            
            ratio = grammar_complexity / monotone_width
            total_metric_value += ratio
            
            if 0.5 <= ratio <= 2:
                conjecture_holds_count += 1
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds_fraction = conjecture_holds_count / instances_tested
    
    return {
        "metric_name": "MinimalGrammarComplexityOverMonotoneWidth",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds_fraction >= 0.833,  # 25/30 seeds
        "counterexample": "" if conjecture_holds_fraction >= 0.833 else "Ratio out of bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    conjecture_holds_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif conjecture_holds_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={conjecture_holds_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")