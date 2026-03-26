import ee


class GEEInitializer:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.initialized = False

    def initialize(self) -> None:
        if not self.initialized:
            ee.Authenticate()
            ee.Initialize(project=self.project_id)
            self.initialized = True