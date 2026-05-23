import numpy as np
from models import TDTLInstance

def calculate_battery_capacity(instance: TDTLInstance) -> float:
    """
    Makale Sayfa 16 Orijinal Formülü:
    Q = (2.0 / n) * Toplam_Drone_Süresi
    """
    if instance.drone_time_matrix is None:
        raise ValueError("Önce süre matrisleri hesaplanmalıdır!")
        
    n = instance.n
    # Tüm satır ve sütunlardaki drone sürelerinin toplamı
    total_drone_time = np.sum(instance.drone_time_matrix)
    
    # Q formülünün koda dökümü
    Q = (2.0 / n) * total_drone_time
    instance.Q = Q
    return Q


def evaluate_solution(truck_route: list, drone_assignments: dict, instance: TDTLInstance):
    """
    İki aşamalı hibrit model veya baseline çıktılarını değerlendirir.
    Kamyon ve drone sürelerini paralel olarak (max kontrolüyle) hesaplar.
    
    :param truck_route: Kamyonun uğrayacağı senkronizasyon düğümleri listesi [0, 8, 6, 2, 9...]
    :param drone_assignments: dict -> key: (A, B) kamyon kenarı, value: [C, D] drone uğrak düğümleri
    :return: makespan (float), feasible (bool), edge_details (list)
    """
    t_T = instance.truck_time_matrix
    t_D = instance.drone_time_matrix
    Q = instance.Q
    
    makespan = 0.0
    is_feasible = True
    edge_details = []
    
    # Kamyon rotasındaki her ardışık senkronizasyon adımı için dön
    for i in range(len(truck_route) - 2):
        A = truck_route[i]
        B = truck_route[i+1]
        
        # 1. Kamyonun direkt A'dan B'ye gitme süresi
        truck_duration = t_T[A][B]
        
        # 2. Drone'un A -> Drone Düğümleri -> B sub-route süresi
        drone_nodes = drone_assignments.get((A, B), [])
        
        if len(drone_nodes) == 0:
            # Eğer bu kenarda drone uçmadıysa, drone kamyonun üzerindedir (Süre = Kamyon süresi)
            drone_duration = 0.0
            stage_duration = truck_duration
        else:
            # Drone rotasının parça parça süre toplanması
            drone_duration = 0.0
            current_node = A
            for next_node in drone_nodes:
                drone_duration += t_D[current_node][next_node]
                current_node = next_node
            drone_duration += t_D[current_node][B] # Son düğümden B'ye dönüş
            
            # PARALEL HESAPLAMA: Kamyon ve drone aynı anda hareket eder, senkronizasyon max() gerektirir
            stage_duration = max(truck_duration, drone_duration)
            
            # Batarya kontrolü (Q kapasitesini aşıp aşmadığı)
            if drone_duration > Q:
                is_feasible = False
                
        makespan += stage_duration
        
        edge_details.append({
            "edge": (A, B),
            "truck_duration": truck_duration,
            "drone_duration": drone_duration,
            "stage_duration": stage_duration,
            "drone_path": drone_nodes
        })
        
    return makespan, is_feasible, edge_details