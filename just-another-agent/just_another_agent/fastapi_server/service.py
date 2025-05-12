

class JustAnotherService:
    def __init__(self, name: str):
        self.name = name

    def start(self):
        print(f"Starting service: {self.name}")

    def stop(self):
        print(f"Stopping service: {self.name}")

    def restart(self):
        print(f"Restarting service: {self.name}")
        
    def status(self):
        print(f"Service {self.name} is running.")