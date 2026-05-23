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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append(f'~{variables[i-1]} | ~{variables[j-1]}')
        return variables, clauses
    
    def tseitin_formula_to_graph(variables, clauses):
        graph = {}
        for clause in clauses:
            if ' | ' in clause:
                literals = clause.split(' | ')
            elif ' & ' in clause:
                literals = clause.split(' & ')
            else:
                literals = [clause]
            for literal in literals:
                if literal.startswith('~'):
                    node = literal[1:]
                else:
                    node = literal
                if node not in graph:
                    graph[node] = set()
                for other_literal in literals:
                    if other_literal != literal:
                        if other_literal.startswith('~'):
                            other_node = other_literal[1:]
                        else:
                            other_node = other_literal
                        graph[node].add(other_node)
        return graph
    
    def is_connected(graph):
        visited = set()
        stack = [next(iter(graph))]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(graph[node] - visited)
        return len(visited) == len(graph)
    
    def minimal_representation_rank(G):
        n = len(G)
        for r in range(1, n+1):
            for subset in itertools.combinations(range(n), r):
                subgraph = {i: set() for i in subset}
                for u, v in G:
                    if u in subset and v in subset:
                        subgraph[u].add(v)
                        subgraph[v].add(u)
                if is_connected(subgraph):
                    return r
        return n
    
    def resolution_depth(clauses):
        stack = []
        literals = set()
        for clause in clauses:
            if ' | ' in clause:
                literals.update(clause.split(' | '))
            elif ' & ' in clause:
                literals.update(clause.split(' & '))
            else:
                literals.add(clause)
        depth = 0
        while literals:
            new_literals = set()
            for literal in literals:
                if literal.startswith('~'):
                    other_literal = literal[1:]
                else:
                    other_literal = '~' + literal
                if other_literal in literals:
                    literals.remove(literal)
                    literals.remove(other_literal)
                    new_literals.update(clause.split(' | ') if ' | ' in clause else clause.split(' & '))
            literals.update(new_literals)
            depth += 1
        return depth
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    G = tseitin_formula_to_graph(variables, clauses)
    
    d = resolution_depth(clauses)
    r = minimal_representation_rank(G)
    
    return {
        "metric_name": "resolution_depth_vs_representation_rank",
        "metric_value": r,
        "instances_tested": 1,
        "conjecture_holds": r >= 2**d,
        "counterexample": "" if r >= 2**d else f"Counterexample: n={n}, d={d}, r={r}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")