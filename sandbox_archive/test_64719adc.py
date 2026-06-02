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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, 3))]
            circuit.append((gate, inputs))
        return circuit
    
    def tseitin_formula(circuit):
        variables = set()
        clauses = []
        
        def assign_variable():
            nonlocal variables
            var = len(variables)
            variables.add(var)
            return var
        
        def negate(var):
            return -var
        
        def add_clause(clause):
            nonlocal clauses
            clauses.append(clause)
        
        def process_gate(gate, inputs):
            if gate == 'AND':
                output_var = assign_variable()
                for input_var in inputs:
                    add_clause([negate(output_var), input_var])
                    add_clause([negate(input_var), output_var])
                return output_var
            elif gate == 'OR':
                output_var = assign_variable()
                for input_var in inputs:
                    add_clause([-output_var, negate(input_var)])
                return output_var
        
        stack = []
        for gate, inputs in reversed(circuit):
            if isinstance(inputs[0], int):
                stack.append(process_gate(gate, inputs))
            else:
                stack.append(inputs)
        
        final_output = stack.pop()
        add_clause([negate(final_output), assign_variable()])
        return clauses
    
    def minimal_order(clauses):
        n = len(variables)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            if len(clause) == 2 and clause[0] < 0:
                matrix[-1][abs(clause[0])] += 1
            else:
                for var in clause:
                    if var > 0:
                        matrix[var - 1][-1] += 1
                        for other_var in clause:
                            if other_var != var and other_var > 0:
                                matrix[var - 1][other_var - 1] -= 1
        
        rank = 0
        for i in range(n):
            if matrix[i][i] == 0:
                found_pivot = False
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
            
            pivot = Fraction(matrix[i][i])
            for j in range(i + 1, n + 1):
                matrix[i][j] /= pivot
        
            for j in range(n):
                if i != j and matrix[j][i] != 0:
                    factor = -matrix[j][i]
                    for k in range(i, n + 1):
                        matrix[j][k] += factor * matrix[i][k]
        
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return rank
    
    def monotone_width(circuit):
        n = len(variables)
        width = [0] * (n + 1)
        
        def process_gate(gate, inputs):
            if gate == 'AND':
                for input_var in inputs:
                    width[input_var] += 1
            elif gate == 'OR':
                max_width = max(width[var] for var in inputs)
                for var in inputs:
                    width[var] = max_width
        
        stack = []
        for gate, inputs in reversed(circuit):
            if isinstance(inputs[0], int):
                process_gate(gate, inputs)
            else:
                stack.append(inputs)
        
        return max(width)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        clauses = tseitin_formula(circuit)
        m_Cphi = minimal_order(clauses)
        w_Cphi = monotone_width(circuit)
        
        if m_Cphi > 10:
            return {
                "metric_name": "m(Cφ)",
                "metric_value": m_Cphi,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"m(Cφ) > 10 for n={n}"
            }
        
        results.append((m_Cphi, w_Cphi))
    
    mean_m = sum(m for m, _ in results) / len(results)
    std_m = math.sqrt(sum((m - mean_m) ** 2 for m, _ in results) / len(results))
    support_fraction = sum(1 for m, w in results if m < 0.5 * w) / len(results)
    
    return {
        "metric_name": "m(Cφ)",
        "metric_value": mean_m,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_m = sum(result["metric_value"] for result in results) / len(results)
    std_m = math.sqrt(sum((result["metric_value"] - mean_m) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_m} std={std_m} support_fraction={support_fraction}")
    elif any(result["counterexample"]):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")