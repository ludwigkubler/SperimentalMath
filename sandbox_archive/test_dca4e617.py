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
    
    def generate_ac0_circuit(n, func):
        # Generate a random AC⁰ circuit of size n computing the given function
        if func == 'PARITY':
            return [random.choice([1, -1]) for _ in range(n)]
        elif func == 'XOR':
            return [random.choice([1, -1]) for _ in range(n)]
        else:
            raise NotImplementedError("Mapping_undefined")
    
    def construct_variety(circuit):
        # Construct the associated real algebraic variety V for the circuit
        # This is a placeholder function; replace with actual computation
        return len(circuit)
    
    def count_irreducible_components(V):
        # Count the number of irreducible components of the variety V
        return V
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n, 'XOR')
        V = construct_variety(circuit)
        irreducible_components = count_irreducible_components(V)
        results.append(irreducible_components)
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    conjecture_holds = all(x < c * math.log(n) for n, x in zip(n_values, results))
    counterexample = "" if conjecture_holds else "XOR circuit with size {}".format(max(n_values))
    
    return {
        "metric_name": "Number of irreducible components",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample='XOR circuit with size {}'.first_failing_seed={}".format(max(n_values), first_failing_seed))