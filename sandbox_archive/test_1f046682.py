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
    
    def dpll(cnf):
        if not cnf:
            return True
        literal = next((lit for lit in range(1, len(cnf) + 1) if all(lit not in clause or -lit not in clause for clause in cnf)), None)
        if literal is None:
            return False
        new_cnf_true = [clause for clause in cnf if literal not in clause]
        new_cnf_false = [clause for clause in cnf if -literal not in clause]
        return dpll(new_cnf_true) or dpll(new_cnf_false)
    
    def generate_circuit(n, k):
        cnf = []
        literals = list(range(1, n + 1))
        while len(cnf) < k:
            new_clause = random.sample(literals, random.randint(1, n))
            if all(all(lit not in clause or -lit not in clause for clause in cnf) for lit in new_clause):
                cnf.append(new_clause)
        return cnf
    
    def graphical_motive(cnf):
        # Simplified representation of the graphical motive
        return len(cnf)
    
    def rank(motive):
        # Rank is simply the size of the motive for this simplified example
        return motive
    
    n = 10
    k = 5
    epsilon = 1e-6
    instances_tested = 30
    min_rank = float('inf')
    
    for _ in range(instances_tested):
        cnf = generate_circuit(n, k)
        motive = graphical_motive(cnf)
        current_rank = rank(motive)
        if current_rank < min_rank:
            min_rank = current_rank
    
    expected_rank = O(k**2 * math.log(n))
    metric_value = abs(min_rank - expected_rank) <= epsilon
    conjecture_holds = metric_value
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank",
        "metric_value": min_rank,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")