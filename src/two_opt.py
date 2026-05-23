import numpy as np
from models import TDTLInstance

def route_cost(route: list, t_T: np.ndarray) -> float:
    """Rotanın toplam kamyon (mesafe) maliyetini hesaplar."""
    cost = 0.0
    for i in range(len(route) - 1):
        cost += t_T[route[i]][route[i+1]]
    return cost

def run_2opt_tsp(instance: TDTLInstance) -> list:
    """
    Tüm düğümleri kapsayan başlangıç bir TSP rotası üretir.
    Origin (0) ve Destination (n-1) sabit tutulur.
    """
    n = instance.n
    t_T = instance.truck_time_matrix
    
    # Başlangıç rotası: 0 -> 1 -> 2 -> ... -> n-1
    best_route = [instance.origin] + list(range(1, n - 1)) + [instance.destination]
    improved = True
    
    while improved:
        improved = False
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                if j - i == 1: continue
                
                # i ve j arasındaki segmenti ters çevir
                new_route = best_route[:]
                new_route[i:j] = reversed(best_route[i:j])
                
                if route_cost(new_route, t_T) < route_cost(best_route, t_T):
                    best_route = new_route
                    improved = True
                    
    return best_route