from dataclasses import dataclass

@dataclass #装饰器,自动为类生成一些特殊方法，如 __init__(), __repr__(), __eq__() 等
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str
    
@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransforamtionArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str