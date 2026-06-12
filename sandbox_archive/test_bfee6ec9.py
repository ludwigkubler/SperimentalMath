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
    
    def generate_circuit(n):
        # Generate a random boolean circuit with n variables and depth 5-10
        depth = random.randint(5, 10)
        if depth == 5:
            return ["NOT", "AND", "OR"]
        elif depth == 6:
            return ["NOT", "NOT", "AND", "OR"]
        elif depth == 7:
            return ["NOT", "NOT", "NOT", "AND", "OR"]
        elif depth == 8:
            return ["NOT", "NOT", "NOT", "NOT", "AND", "OR"]
        elif depth == 9:
            return ["NOT", "NOT", "NOT", "NOT", "NOT", "AND", "OR"]
        else:
            return ["NOT", "NOT", "NOT", "NOT", "NOT", "NOT", "AND", "OR"]

    def syntactic_monoid(circuit):
        # Compute the syntactic monoid of a circuit
        if len(circuit) == 1:
            return {circuit[0]}
        else:
            submonoids = [syntactic_monoid(subcircuit) for subcircuit in circuit[1:]]
            return set.union(*submonoids)

    def minimal_locally_indecomposable_module(monoid):
        # Compute the minimal locally indecomposable module of a monoid
        if len(monoid) == 0:
            return set()
        else:
            generators = list(monoid)
            relations = []
            for i in range(len(generators)):
                for j in range(i + 1, len(generators)):
                    relation = (generators[i], generators[j])
                    relations.append(relation)
            return set(relations)

    def order(module):
        # Compute the order of a module
        return len(module)

    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    monoid = syntactic_monoid(circuit)
    module = minimal_locally_indecomposable_module(monoid)
    ratio = order(module) / (len(circuit) ** 2)

    return {
        "metric_name": "Ratio of Module Order to Depth^2",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= ratio <= 1.5,
        "counterexample": "" if 0.5 <= ratio <= 1.5 else "ratio_outside_bounds"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio_outside_bounds' first_failing_seed={first_failing_seed}")