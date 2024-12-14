from deployment.custom_logging import error_logger

# Custom exception handler function
def handle_exception(error, error_type):
    """
    Logs the error with details to the log file and prints a formatted message to the console.
    
    Args:
        error (Exception): The original exception instance.
        error_type (PipelineError): The specific pipeline error type (e.g., PRedictionError).
    """
    # Log the complete stack trace and details to the log file
    error_logger.error("Exception occurred", exc_info=True)

    error_logger.error("\n\n")  # To leave a few blank lines

    # Print only the formatted message to the console
    print(f"{error_type.__name__}: {error.__class__.__name__}: {error}")



# Base custom exception
class PipelineError(Exception):
    """Base class for custom pipeline exceptions"""
    def __init__(self, original_exception):
        super().__init__(str(original_exception))
        self.original_exception = original_exception

# Specific pipeline exceptions
class FeatureEngineeringError(PipelineError):
    pass

class PredictionError(PipelineError):
    pass

class BayesianOptimizationError(PipelineError):
    pass

if __name__ == "__main__":
    try:
        my_func(23)
    except Exception as e:
        handle_exception(e, PredictionError)