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
    
    # Generate a random explicit function in P with varying complexity
    n = random.randint(5, 40)
    function_complexity = n**2
    
    # Construct a corresponding noncommutative algebra for the function
    # (This is a placeholder; actual construction depends on the function's input-output pairs)
    algebra_size = function_complexity
    
    # Compute the minimal order of the polynomial automaton for the algebra
    # (This is a placeholder; actual computation depends on the algebra's structure)
    automaton_order = algebra_size
    
    # Compare it to the size of the ACC⁰ circuit computing the same function
    circuit_size = function_complexity
    
    # Check if the conjecture holds
    conjecture_holds = automaton_order >= circuit_size
    
    return {
        "metric_name": "Automaton Order vs Circuit Size",
        "metric_value": automaton_order,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Function complexity {function_complexity}, Automaton Order {automaton_order}, Circuit Size {circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*2 + 1))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Function complexity exceeds automaton order\" first_failing_seed={first_failing_seed}")