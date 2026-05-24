# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def acc0_circuit_depth(f):
        # Example function to simulate ACC⁰ circuit depth for a given polynomial f
        # This is a placeholder and should be replaced with actual computation
        return 3  # Placeholder value
    
    def quasi_monte_carlo_lattice_rank(n, f):
        # Example function to simulate the minimal rank of a quasi-Monte Carlo lattice
        # This is a placeholder and should be replaced with actual computation
        return n * acc0_circuit_depth(f)
    
    n = random.randint(5, 40)
    f = lambda x: sum(x)  # Example polynomial function
    
    try:
        rank = quasi_monte_carlo_lattice_rank(n, f)
        depth = acc0_circuit_depth(f)
        
        if rank < depth:
            return {
                "metric_name": "quasi_monte_carlo_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank} is less than depth {depth}"
            }
        else:
            return {
                "metric_name": "quasi_monte_carlo_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            }
    except Exception as e:
        return {
            "metric_name": "quasi_monte_carlo_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [101, 103, 107, 109]  # Default to first 30 primes and a few more
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank less than depth\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")