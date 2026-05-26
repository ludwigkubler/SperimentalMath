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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def frege_proof_width(formula):
        # Simplified Frege proof width calculation
        return len(formula) ** 0.5
    
    def graphical_subgroup_action(graph):
        subgroup_order = 1
        for node in graph:
            neighbors = [n for n in range(len(graph)) if (node, n) in graph or (n, node) in graph]
            subgroup_order *= len(neighbors)
        return subgroup_order
    
    def is_valid_sat_instance(instance):
        # Simplified SAT instance validation
        return all(isinstance(x, bool) for x in instance)
    
    def sat_to_graph(sat_instance):
        n = int(math.sqrt(len(sat_instance)))
        graph = set()
        for i in range(n * n):
            if sat_instance[i]:
                row, col = divmod(i, n)
                for j in range(col + 1, n):
                    graph.add((row * n + col, row * n + j))
                for j in range(row + 1, n):
                    graph.add((row * n + col, j * n + col))
        return graph
    
    def run_trial(seed: int) -> dict:
        random.seed(seed)
        
        n = random.randint(5, 40)
        graph = generate_graph(n)
        subgroup_order = graphical_subgroup_action(graph)
        
        if subgroup_order == 0:
            return {
                "metric_name": "Frege Proof Width",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "subgroup_order_zero"
            }
        
        sat_instance = [random.choice([True, False]) for _ in range(n * n)]
        if not is_valid_sat_instance(sat_instance):
            return {
                "metric_name": "Frege Proof Width",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "invalid_sat_instance"
            }
        
        graph_from_sat = sat_to_graph(sat_instance)
        frege_width = frege_proof_width(graph_from_sat)
        
        if subgroup_order > 2 ** (math.log2(frege_width) + 1):
            return {
                "metric_name": "Frege Proof Width",
                "metric_value": frege_width,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"subgroup_order={subgroup_order}, frege_width={frege_width}"
            }
        
        return {
            "metric_name": "Frege Proof Width",
            "metric_value": frege_width,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    conjecture_holds = all(r["conjecture_holds"] for r in results if r["instances_tested"] > 0)
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")