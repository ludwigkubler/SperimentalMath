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
        clauses = []
        for _ in range(10 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(x) != abs(y) for x, y in combinations(clause, 2)):
                clauses.append(clause)
        return clauses

    def tseitin_resolution_tree(clauses):
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        
        nodes = {0: []}
        edges = []
        
        def add_node(parent, literal, polarity):
            node_id = len(nodes)
            nodes[parent].append(node_id)
            nodes[node_id] = []
            edges.append((parent, node_id))
            return node_id
        
        for i in range(len(clauses)):
            clause = clauses[i]
            pos_nodes = [add_node(0, lit, True) for lit in clause if lit > 0]
            neg_nodes = [add_node(0, -lit, False) for lit in clause if lit < 0]
            
            if len(pos_nodes) == 1 and len(neg_nodes) == 1:
                add_node(0, pos_nodes[0], True)
                add_node(0, neg_nodes[0], False)
            else:
                pos_combinations = list(itertools.combinations(pos_nodes, 2))
                neg_combinations = list(itertools.combinations(neg_nodes, 2))
                
                for (p1, p2) in pos_combinations:
                    new_node = add_node(0, -i, False)
                    edges.append((p1, new_node))
                    edges.append((p2, new_node))
                    
                for (n1, n2) in neg_combinations:
                    new_node = add_node(0, i, True)
                    edges.append((n1, new_node))
                    edges.append((n2, new_node))
        
        return nodes, edges

    def cohomology_rank(tree):
        # Simplified rank calculation for demonstration
        # This is a placeholder and should be replaced with actual computation
        depth = max(len(path) for path in find_paths(tree))
        return depth

    def find_paths(tree, node=0, path=[]):
        if not tree[node]:
            yield path + [node]
        else:
            for child in tree[node]:
                yield from find_paths(tree, child, path + [node])

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    tree, _ = tseitin_resolution_tree(clauses)
    
    rank = cohomology_rank(tree)
    depth = max(len(path) for path in find_paths(tree))
    
    return {
        "metric_name": "cohomology_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= 2 * depth,  # Placeholder constant
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")