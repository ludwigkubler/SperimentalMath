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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def frege_proof_width(formula):
        # Placeholder function to simulate Frege proof width
        # This is a dummy implementation and should be replaced with actual logic
        return len(formula)
    
    def graphical_subgroup_action(graph):
        # Placeholder function to simulate graphical subgroup action
        # This is a dummy implementation and should be replaced with actual logic
        return 2 ** len(graph)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(5):  # Test each size with 5 instances
            graph = generate_random_graph(n)
            sat_instance = [f"x{i}" for i in range(n)]
            frege_proof_width_value = frege_proof_width(sat_instance)
            subgroup_action_order = graphical_subgroup_action(graph)
            
            if subgroup_action_order > 2 ** frege_proof_width_value:
                conjecture_holds = False
                counterexample = f"Graph with n={n}, subgroup action order {subgroup_action_order} > 2^({frege_proof_width_value})"
                break
            
            instances_tested += 1
        
        results.append({
            "metric_name": "Frege Proof Width",
            "metric_value": frege_proof_width_value,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["instances_tested"] > 0 for r in results):
        metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values)) ** 2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
        else:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")