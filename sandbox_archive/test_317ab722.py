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

def generate_cnf(n):
    cnf = []
    for _ in range(10 * n):  # Generate a CNF with 10 clauses per variable on average
        clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)
                   for _ in range(random.randint(2, 4))]
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    literals = set()
    queue = []
    for clause in cnf:
        if len(clause) == 1:
            literals.add(clause[0])
        else:
            queue.append(clause)
    
    while queue:
        clause = queue.pop(0)
        literal_to_remove = None
        for lit in clause:
            if -lit in literals:
                literal_to_remove = lit
                break
        if literal_to_remove is not None:
            literals.remove(-literal_to_remove)
            new_clauses = []
            for other_clause in cnf:
                if literal_to_remove in other_clause:
                    continue
                if -literal_to_remove in other_clause:
                    other_clause.remove(-literal_to_remove)
                    if len(other_clause) == 1:
                        literals.add(other_clause[0])
                    else:
                        new_clauses.append(other_clause)
            queue.extend(new_clauses)
        else:
            return float('inf')
    
    return max(len(literals), 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if width < 1.5 * math.log(n) / math.log(math.log(n)) else True,
        "counterexample": "" if width >= 1.5 * math.log(n) / math.log(math.log(n)) else f"width={width}, expected>=1.5*log({n})/log(log({n}))={1.5 * math.log(n) / math.log(math.log(n))}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(seeds) if not run_trial(r)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")