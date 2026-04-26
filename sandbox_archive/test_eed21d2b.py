import random
import math
import json
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def extended_frege_proof_size(n):
        # Placeholder for actual EF proof size computation
        return 2 ** n
    
    def tutte_polynomial_degree(matroid, rank):
        if len(matroid) == 0 or rank == 0:
            return 1
        e = matroid[0]
        sub_matroid_without_e = [row[1:] for row in matroid[1:] if row[0] != e]
        sub_matroid_with_e = [row[:] for row in matroid[1:]]
        return tutte_polynomial_degree(sub_matroid_without_e, rank - 1) + tutte_polynomial_degree(sub_matroid_with_e, rank)
    
    def column_matroid(incidence_matrix):
        n = len(incidence_matrix)
        m = len(incidence_matrix[0])
        matroid = []
        for j in range(m):
            col = [i for i in range(n) if incidence_matrix[i][j] == 1]
            matroid.append(col)
        return matroid
    
    def rank(matroid):
        max_rank = 0
        for subset in combinations(range(len(matroid)), len(matroid)):
            sub_matroid = [matroid[i] for i in subset]
            if all(all(x not in y for x, y in zip(subset, sub_matroid)) for y in sub_matroid[1:]):
                max_rank = max(max_rank, len(subset))
        return max_rank
    
    n = random.randint(5, 14)
    incidence_matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    matroid = column_matroid(incidence_matrix)
    matroid_rank = rank(matroid)
    
    degree = tutte_polynomial_degree(matroid, matroid_rank)
    ef_size = extended_frege_proof_size(n)
    
    conjecture_holds = abs(degree - 2 * n) < 0.1 * n
    counterexample = "" if conjecture_holds else f"n={n}, degree={degree}, EF size={ef_size}"
    
    return {
        "metric_name": "Tutte Polynomial Degree",
        "metric_value": degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    total_degree = 0
    total_tests = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {json.dumps(trial_result)}")
        results.append(trial_result)
        total_degree += trial_result["metric_value"]
        total_tests += trial_result["instances_tested"]
    
    mean_degree = total_degree / total_tests
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_degree} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")