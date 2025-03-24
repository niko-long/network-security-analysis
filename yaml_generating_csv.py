import pandas as pd
import yaml
import os

def generate_schema():
    # 读取 CSV 文件
    FILE_PATH_1 = os.path.join(os.getcwd(), "Network_Data", "phisingData.csv")  
    df = pd.read_csv(FILE_PATH_1)

    # 生成 YAML schema
    schema = {
        "columns": [{col: str(df[col].dtype)} for col in df.columns],  # 使用列表生成每一列的键值对
        "numerical_columns": df.select_dtypes(include=['number']).columns.tolist()  # 仅选择数值型列
    }

    # 自定义 YAML 输出格式
    schema_yaml = yaml.dump(schema, default_flow_style=False, sort_keys=False, indent=4)

    # 处理 "numerical_columns" 和 "columns" 部分，确保每个项目前有'-'
    # 先转换 "columns" 部分为想要的格式
    columns_yaml = "columns:\n"
    for col in df.columns:
        columns_yaml += f"  - {col}: {str(df[col].dtype)}\n"

    # 然后处理 "numerical_columns" 部分
    numerical_columns_yaml = "numerical_columns:\n"
    for col in schema["numerical_columns"]:
        numerical_columns_yaml += f"  - {col}\n"

    # 将 "columns" 和 "numerical_columns" 部分拼接到一起
    final_yaml = columns_yaml + numerical_columns_yaml

    # 确保文件保存到正确位置
    folder_path = os.path.join(os.getcwd(), "data_schema")  
    os.makedirs(folder_path, exist_ok=True)

    # 完整的文件路径
    file_path = os.path.join(folder_path, "schema.yaml")

    # 保存 YAML 到文件
    with open(file_path, "w") as f:
        f.write(final_yaml)

    print("schema.yaml 生成成功！")

if __name__ == '__main__':
    generate_schema()
