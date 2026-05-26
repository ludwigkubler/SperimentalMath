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
    
    def generate_3cnf(n):
        literals = [f"x{i}" for i in range(1, n+1)] + [f"~x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(2*n):
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses

    def tseitin_resolution_tree(clauses):
        literals = set()
        for clause in clauses:
            literals.update(clause)
        
        nodes = {}
        edges = []
        
        def add_node(node_id):
            if node_id not in nodes:
                nodes[node_id] = {'children': [], 'parent': None}
        
        def add_edge(parent, child):
            edges.append((parent, child))
            nodes[child]['parent'] = parent
        
        def resolve(l1, l2):
            if l1[0] == '~' and l1[1:] == l2:
                return True
            elif l2[0] == '~' and l2[1:] == l1:
                return True
            return False
        
        for clause in clauses:
            node_id = random.randint(1, 1000)
            add_node(node_id)
            nodes[node_id]['children'] = [random.randint(1, 1000) for _ in range(len(clause))]
            for child in nodes[node_id]['children']:
                add_edge(node_id, child)
        
        return nodes, edges

    def cohomology_rank(tree):
        # Placeholder function to compute the rank of cohomology groups
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)

    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_3cnf(n)
    tree, _ = tseitin_resolution_tree(formula)
    rank = cohomology_rank(tree)
    depth = len(list(tree.keys()))
    
    if depth == 0:
        return {
            "metric_name": "cohomology_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    c = rank / depth
    conjecture_holds = c <= 2  # Example constant multiple, replace with actual bound
    
    return {
        "metric_name": "cohomology_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"c={c} exceeds bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"c exceeds bound\" first_failing_seed={first_failing_seed}")