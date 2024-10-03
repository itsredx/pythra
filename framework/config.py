import yaml

class Config:

    _instance = None  # Class-level attribute to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If an instance doesn't exist, create one
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance  # Return the singleton instance

    def __init__(self, config_file='config.yaml'):
        # Only initialize the instance once
        if not hasattr(self, 'initialized'):
            self.initialized = True  # Mark the instance as initialized
            with open(config_file, 'r') as file:
                self.config = yaml.safe_load(file)

    def get(self, key, default=None):
        return self.config.get(key, default)

