class EnergyMonitor:
    def __init__(self, available_joules=10.0):
        self.available_joules = available_joules

    def available_energy(self):
        return self.available_joules
