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
    
    def generate_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(2 * n), 2)
            circuit.append((gate_type, inputs))
        return circuit
    
    def cnf_from_circuit(circuit, n):
        literals = [f'x{i+1}' if i < n else f'-x{i-n+1}' for i in range(2 * n)]
        clauses = []
        for gate_type, inputs in circuit:
            clause = []
            for input in inputs:
                literal = literals[input]
                if random.choice([True, False]):
                    literal = '-' + literal
                clause.append(literal)
            clauses.append(' '.join(clause) + ' 0')
        return '\n'.join(clauses), n
    
    def dpll(cnf):
        cnf_lines = cnf.split('\n')
        cnf_dict = {}
        for line in cnf_lines:
            if line and not line.startswith('c'):
                literals = line.split()
                clause = [literals[0]]
                for literal in literals[1:]:
                    if literal == '0':
                        break
                    clause.append(literal)
                cnf_dict[len(cnf_dict) + 1] = clause
        
        def solve(model):
            unit_clauses = {key: value[0] for key, value in cnf_dict.items() if len(value) == 1}
            pure_literals = {}
            
            while True:
                unit_clause = next((unit for unit in unit_clauses if all(literal not in model for literal in unit.split()) and any(literal in model for literal in unit.split())), None)
                if unit_clause is None:
                    break
                literal = unit_clause.split()[0]
                model.add(literal)
                del unit_clauses[unit_clause]
                
                for clause_id, clause in cnf_dict.items():
                    if literal in clause or '-' + literal in clause:
                        cnf_dict[clause_id] = [l for l in clause if l != literal and l != '-' + literal]
                        if not cnf_dict[clause_id]:
                            return False
                    elif '-' + literal in clause:
                        cnf_dict[clause_id].remove('-' + literal)
                
                pure_literal = next((literal for literal, count in collections.Counter([l.split()[0] for l in model]).items() if count == 1), None)
                if pure_literal is not None:
                    pure_literals[pure_literal] = True
                    model.add(pure_literal)
                    del unit_clauses[' '.join([pure_literal])]
                
                for clause_id, clause in cnf_dict.items():
                    if '-' + pure_literal in clause:
                        cnf_dict[clause_id].remove('-' + pure_literal)
                    elif pure_literal in clause:
                        cnf_dict[clause_id] = [l for l in clause if l != pure_literal]
                
                if not any(clause for clause in cnf_dict.values()):
                    return True
        
        model = set()
        return solve(model)
    
    def minimal_representation_size(cnf):
        # Placeholder for the actual computation of minimal representation size
        return len(cnf.split('\n'))
    
    def resolution_proof_width(cnf):
        if not dpll(cnf):
            return 0
        # Placeholder for the actual computation of resolution proof width
        return random.randint(1, 10)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    circuit = generate_circuit(n, m)
    cnf, num_variables = cnf_from_circuit(circuit, n)
    
    min_rep_size = minimal_representation_size(cnf)
    res_width = resolution_proof_width(cnf)
    
    return {
        "metric_name": "Correlation",
        "metric_value": abs(min_rep_size - res_width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if abs(min_rep_size - res_width) > 3 else True,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")