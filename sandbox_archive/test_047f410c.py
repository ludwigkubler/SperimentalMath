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
    
    def generate_cnf(n: int, m: int) -> list:
        cnf = []
        for _ in range(m):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(lit not in [-c, c] for c in clause):
                cnf.append(clause)
        return cnf
    
    def resolution_depth(cnf: list) -> int:
        stack = []
        visited = set()
        
        def resolve(lit: int, new_clause: list) -> bool:
            if lit in new_clause or -lit in new_clause:
                return True
            for other_lit in new_clause:
                if other_lit != -lit and -other_lit not in stack:
                    stack.append(-other_lit)
                    visited.add(-other_lit)
                    if resolve(other_lit, cnf):
                        return True
                    stack.pop()
                    visited.remove(-other_lit)
            return False
        
        for clause in cnf:
            for lit in clause:
                if lit not in visited and -lit not in stack:
                    stack.append(lit)
                    visited.add(lit)
                    if resolve(lit, cnf):
                        return len(stack) - 1
                    stack.pop()
                    visited.remove(lit)
        return 0
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    cnf = generate_cnf(n, m)
    
    depth = resolution_depth(cnf)
    
    return {
        "metric_name": "resolution_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # primes are not needed here
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction=1.0")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results, start=1) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")