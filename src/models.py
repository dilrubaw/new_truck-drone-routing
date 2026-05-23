import numpy as np

class TDTLInstance:
    """
    Truck-Drone Team Logistics (TDTL) Problem Örneği Veri Yapısı.
    """
    def __init__(self, name: str, nodes: np.ndarray, alpha: float):
        """
        :param name: Dosya/Örnek adı (Örn: Uniform, 1-Center)
        :param nodes: (n, 2) boyutunda her düğümün X, Y koordinatlarını tutan matris
        :param alpha: Drone/Truck hız oranı (v_D / v_T) -> {1, 2, 3}
        """
        self.name = name
        self.nodes = nodes
        self.n = len(nodes)  # Toplam düğüm sayısı (n)
        self.alpha = alpha
        
        # Origin (Depot) her zaman ilk düğüm, Destination ise son düğümdür
        self.origin = 0
        self.destination = self.n - 1
        
        # Süre matrisleri ve Batarya Kapasitesi (Q) başlangıçta boş atanır
        self.truck_time_matrix = None
        self.drone_time_matrix = None
        self.Q = 0.0

    def __repr__(self):
        return f"<TDTLInstance: {self.name}, Nodes(n)={self.n}, Alpha={self.alpha}, Q={self.Q:.2f}>"