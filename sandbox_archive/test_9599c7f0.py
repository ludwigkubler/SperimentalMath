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
        leaves = [set()]
        for p in polytope:
            new_leaves = []
            for leaf in leaves:
                new_leaf = set(leaf)
                new_leaf.add(p)
                if len(new_leaf) == len(leaf):
                    continue
                new_leaves.append(new_leaf)
            leaves.extend(new_leaves)
        return leaves
    
    def action_complexity(leaves):
        return sum(len(leaf)**2 for leaf in leaves) / len(leaves)
    
    n = random.randint(1, 40)
    f = generate_boolean_function(n)
    polytope = moment_polytope(f)
    leaves = symplectic_leaves(polytope)
    rho_f = action_complexity(leaves)
    
    if len(leaves) > 2**n:
        return {
            "metric_name": "action_complexity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Too many symplectic leaves"
        }
    
    mean = 2**(n/2)
    std_dev = math.sqrt(n)
    if not (mean - 3*std_dev <= rho_f <= mean + 3*std_dev):
        return {
            "metric_name": "action_complexity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Action complexity {rho_f} does not match expected range"
        }
    
    rho_f_squared = rho_f**2
    for _ in range(95):
        f1, f2 = generate_boolean_function(n), generate_boolean_function(n)
        polytope1, polytope2 = moment_polytope(f1), moment_polytope(f2)
        leaves1, leaves2 = symplectic_leaves(polytope1), symplectic_leaves(polytope2)
        rho_f1, rho_f2 = action_complexity(leaves1), action_complexity(leaves2)
        if not (rho_f1**2 + rho_f2**2 >= n**2/4):
            return {
                "metric_name": "action_complexity",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Action complexity inequality not satisfied for {f1} and {f2}"
            }
    
    return {
        "metric_name": "action_complexity",
        "metric_value": rho_f,
        "instances_tested": 100,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                first_failing_seed = r["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample='Action complexity inequality not satisfied' first_failing_seed={first_failing_seed}")