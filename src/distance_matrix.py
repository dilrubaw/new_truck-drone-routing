import numpy as np
from models import TDTLInstance

def calculate_tdtl_matrices(instance: TDTLInstance) -> TDTLInstance:
    """
    Düğümler arasındaki Euclidean mesafeleri hesaplar, kamyon ve drone süre matrislerini oluşturur.
    Makale kuralı: 
    - t_ij^T = Euclidean_Distance(i, j)
    - t_ij^D = t_ij^T / alpha
    """
    n = instance.n
    truck_matrix = np.zeros((n, n))
    drone_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i == j:
                truck_matrix[i][j] = 0.0
                drone_matrix[i][j] = 0.0
            else:
                # Euclidean mesafesi hesaplama
                coord_i = instance.nodes[i]
                coord_j = instance.nodes[j]
                distance = np.sqrt(np.sum((coord_i - coord_j) ** 2))
                
                # Kamyon süresi direkt mesafeye eşittir (v_T = 1 kabul edilir)
                truck_matrix[i][j] = distance
                
                # Drone süresi kamyon süresinin alpha oranına bölünmesidir (t^D = t^T / alpha)
                drone_matrix[i][j] = distance / instance.alpha
                
    instance.truck_time_matrix = truck_matrix
    instance.drone_time_matrix = drone_matrix
    
    return instance