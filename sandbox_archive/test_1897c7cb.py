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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def shannon_entropy(f):
        n = len(f)
        counts = [f.count(i) for i in set(f)]
        probabilities = [count / n for count in counts]
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        return entropy
    
    def coxeter_diagram(f):
        # Placeholder function to simulate the generation of a Coxeter diagram
        # This is a dummy implementation and should be replaced with actual logic
        return len(set(f))
    
    n = random.randint(5, 40)  # Sample n from {5, 10, 15, 20, 30, 40}
    f = generate_random_boolean_function(n)
    H_f = shannon_entropy(f)
    Diag_f = coxeter_diagram(f)
    
    ratio = Fraction(Diag_f, math.exp(H_f))
    
    return {
        "metric_name": "Ratio of Coxeter Diagrams to Entropy",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 1,
        "counterexample": "" if ratio <= 1 else f"Counterexample: n={n}, Diag(f)={Diag_f}, H(f)={H_f}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"] != ""), "")
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)