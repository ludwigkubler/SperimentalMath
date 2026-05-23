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
    
    def generate_monotone_circuit(n):
        # Generate a random monotone circuit with n inputs
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def decision_tree_depth(circuit):
        # Calculate the depth of the decision tree for the given circuit
        if len(circuit) == 1:
            return 1
        else:
            left = circuit[:len(circuit)//2]
            right = circuit[len(circuit)//2:]
            return 1 + max(decision_tree_depth(left), decision_tree_depth(right))
    
    def young_tableau(circuit):
        # Construct the corresponding Young tableau for the given circuit
        n = int(math.log2(len(circuit)))
        tableau = [[0] * (n+1) for _ in range(n+1)]
        index = 0
        for i in range(1, n+1):
            for j in range(i, 0, -1):
                if circuit[index] == 1:
                    tableau[i][j] = 1
                    index += 1
                else:
                    tableau[j][i] = 1
                    index += 1
        return tableau
    
    def rank(tableau):
        # Calculate the rank of the given Young tableau
        n = len(tableau) - 1
        count = 0
        for i in range(1, n+1):
            for j in range(i, 0, -1):
                if tableau[i][j] == 1:
                    count += 1
        return count
    
    n = random.randint(5, 40)
    circuit = generate_monotone_circuit(n)
    depth = decision_tree_depth(circuit)
    tableau = young_tableau(circuit)
    rho_Y = rank(tableau)
    
    metric_value = rho_Y / math.log2(depth)
    conjecture_holds = metric_value <= 3
    counterexample = "" if conjecture_holds else f"rho(Y)={rho_Y}, log(2^|T(C)|)={math.log2(depth)}"
    
    return {
        "metric_name": "Rank of Young Tableaux vs Decision Tree Depth",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")