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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def moment_polytope(f):
        n = int(math.log2(len(f)))
        polytope = []
        for i in range(2**n):
            if f[i] == 1:
                polytope.append(i)
        return polytope
    
    def symplectic_leaves(polytope):
        leaves = []
        for i in range(len(polytope)):
            leaf = [polytope[i]]
            for j in range(i+1, len(polytope)):
                if (polytope[j] & polytope[i]) == 0:
                    leaf.append(polytope[j])
            leaves.append(leaf)
        return leaves
    
    def action_complexity(leaves):
        return sum(len(leaf) for leaf in leaves)
    
    n = random.randint(1, 40)
    f = generate_boolean_function(n)
    polytope = moment_polytope(f)
    leaves = symplectic_leaves(polytope)
    rho_f = action_complexity(leaves)
    
    mean = 2**(n/2)
    std_dev = math.sqrt(n)
    if not (mean - 3*std_dev <= rho_f <= mean + 3*std_dev):
        return {
            "metric_name": "Action Complexity",
            "metric_value": rho_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Action complexity does not follow the Gaussian distribution."
        }
    
    return {
        "metric_name": "Action Complexity",
        "metric_value": rho_f,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Action complexity does not follow the Gaussian distribution.' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")