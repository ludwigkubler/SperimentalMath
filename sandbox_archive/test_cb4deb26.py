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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def braid_representation(cnf, n):
        # Simplified mapping to generate a braids representation
        braids = []
        for clause in cnf:
            braid = []
            for lit in clause:
                if lit > 0:
                    braid.append(f"b_{lit}")
                else:
                    braid.append(f"b_{abs(lit)}^-1")
            braids.append(" * ".join(braid))
        return " + ".join(braids)
    
    def count_non_commuting_generators(braid):
        # Simplified counting of non-commuting generators
        generators = set()
        for term in braid.split(" * "):
            if term.startswith("b_"):
                generators.add(term[2:])
        return len(generators)
    
    n_max = 0
    instances_tested = 0
    total_value = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(1, n)
            cnf = generate_cnf(m, n)
            braid = braid_representation(cnf, n)
            non_commuting_generators = count_non_commuting_generators(braid)
            
            upper_bound = 2**(m+n) / math.factorial(n)
            lower_bound = 3**n
            
            if non_commuting_generators < lower_bound:
                return {
                    "metric_name": "non_commuting_generators",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"Lower bound violated for n={n}, m={m}"
                }
            
            total_value += non_commuting_generators
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    mean_value = total_value / instances_tested
    conjecture_holds = all(0.9 * lower_bound <= mean_value <= upper_bound for _ in range(instances_tested))
    
    return {
        "metric_name": "non_commuting_generators",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Lower bound violated\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unmet_acceptance_criterion")