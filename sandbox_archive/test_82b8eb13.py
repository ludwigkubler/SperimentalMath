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
    
    def generate_random_graph(n):
        edges = set()
        while len(edges) < n * (n - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return [list(u) for u in edges]
    
    def frege_proof_width(formula):
        # Simplified Frege proof width calculation
        return len(formula)
    
    def graphical_subgroup_action(graph):
        n = len(graph)
        subgroup = set()
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in graph or (j, i) in graph:
                    subgroup.add((i, j))
        return len(subgroup)
    
    def sat_instance(graph):
        # Simplified SAT instance generation
        n = len(graph)
        variables = [f"x{i}" for i in range(n)]
        clauses = []
        for u, v in graph:
            clauses.append(f"{variables[u]} | {variables[v]}")
        return " & ".join(clauses)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            graph = generate_random_graph(n)
            subgroup_order = graphical_subgroup_action(graph)
            sat_formula = sat_instance(graph)
            frege_width = frege_proof_width(sat_formula.split(" & "))
            results.append((subgroup_order, frege_width))
    
    total_subgroup_order = sum(order for order, _ in results)
    total_frege_width = sum(width for _, width in results)
    mean_subgroup_order = total_subgroup_order / len(results)
    mean_frege_width = total_frege_width / len(results)
    
    c = math.log2(mean_subgroup_order) / mean_frege_width if mean_frege_width > 0 else float('inf')
    
    conjecture_holds = all(order <= 2**c * width for order, width in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Frege Proof Width",
        "metric_value": mean_frege_width,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")