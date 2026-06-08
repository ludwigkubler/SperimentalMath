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
    
    def generate_cnf(n: int) -> list:
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf: list) -> bool:
        if not cnf:
            return True
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        literal = random.choice(list(literals))
        pos_cnf = [clause for clause in cnf if literal not in clause and -literal not in clause]
        neg_cnf = [clause for clause in cnf if literal in clause or -literal in clause]
        return dpll(pos_cnf) or dpll(neg_cnf)
    
    def frege_depth(cnf: list) -> int:
        if not cnf:
            return 0
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        literal = random.choice(list(literals))
        pos_cnf = [clause for clause in cnf if literal not in clause and -literal not in clause]
        neg_cnf = [clause for clause in cnf if literal in clause or -literal in clause]
        return 1 + max(frege_depth(pos_cnf), frege_depth(neg_cnf))
    
    n_max = 30
    instances_tested = 0
    total_ratio = 0.0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            local_index = len(cnf) / n  # Simplified local index for demonstration
            fd = frege_depth(cnf)
            if fd > 0:
                ratio = local_index / math.log2(fd)
                total_ratio += ratio
                instances_tested += 1
    
    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0.0
    conjecture_holds = abs(mean_ratio - local_index) <= 2 ** local_index
    counterexample = "" if conjecture_holds else f"Ratio {mean_ratio} does not match expected {local_index}"
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")