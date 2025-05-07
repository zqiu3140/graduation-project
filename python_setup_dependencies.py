import os
import sys
import re
import subprocess
import pkg_resources

def get_installed_packages():
    """取得已安裝的套件清單"""
    return {pkg.key for pkg in pkg_resources.working_set}

def scan_imports(file_path):
    """掃描Python檔案中的import語句"""
    imports = set()
    
    # 讀取檔案內容
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except:
        print(f"無法讀取檔案: {file_path}")
        return imports
    
    # 匹配import語句
    import_patterns = [
        r'^import\s+([a-zA-Z0-9_]+)',  # import xxx
        r'^from\s+([a-zA-Z0-9_]+)\s+import',  # from xxx import
    ]
    
    for pattern in import_patterns:
        matches = re.findall(pattern, content, re.MULTILINE)
        for match in matches:
            # 排除標準庫和本地模組
            if not match.startswith(('os', 'sys', 're', 'uuid', 'datetime', 'collections', 
                                     'tempfile', 'typing', 'itertools')) and '.' not in match:
                imports.add(match)
    
    return imports

def find_python_files(root_dir):
    """遞迴查找所有Python檔案"""
    python_files = []
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                python_files.append(os.path.join(dirpath, filename))
    
    return python_files

def map_import_to_package(import_name):
    """將import名稱映射到pip包名稱"""
    mapping = {
        'ckip_transformers': 'ckip-transformers',
        'firebase_admin': 'firebase-admin',
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'mysql': 'mysql-connector-python',
        'reportlab': 'reportlab',
        'Levenshtein': 'python-Levenshtein',
        'pypinyin': 'pypinyin',
        'torch': 'torch',
        'pydantic': 'pydantic',
    }
    
    return mapping.get(import_name, import_name)

def install_package(package_name):
    """使用pip安裝套件"""
    print(f"正在安裝 {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✓ {package_name} 安裝成功")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ {package_name} 安裝失敗")
        return False

def main():
    print("=== 自動依賴庫安裝工具 ===")
    
    # 取得專案根目錄
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"掃描專案目錄: {root_dir}")
    
    # 找出所有Python檔案
    python_files = find_python_files(root_dir)
    print(f"找到 {len(python_files)} 個Python檔案")
    
    # 掃描所有import語句
    all_imports = set()
    for file_path in python_files:
        imports = scan_imports(file_path)
        all_imports.update(imports)
    
    # 將import名稱映射到pip包名稱
    packages_to_install = {map_import_to_package(imp) for imp in all_imports}
    
    # 檢查已安裝的套件
    installed_packages = get_installed_packages()
    packages_to_install = {pkg for pkg in packages_to_install if pkg.lower() not in installed_packages}
    
    if not packages_to_install:
        print("所有依賴庫已安裝")
        return
    
    print(f"\n需要安裝的套件: {', '.join(packages_to_install)}")
    
    # 詢問使用者是否安裝
    choice = input("是否安裝這些套件? (y/n): ")
    if choice.lower() != 'y':
        print("安裝已取消")
        return
    
    # 安裝套件
    installed = []
    failed = []
    for package in packages_to_install:
        if install_package(package):
            installed.append(package)
        else:
            failed.append(package)
    
    # 生成requirements.txt
    if installed:
        req_path = os.path.join(root_dir, 'requirements.txt')
        with open(req_path, 'w', encoding='utf-8') as f:
            for package in sorted(installed):
                f.write(f"{package}\n")
        print(f"\n已生成 requirements.txt 檔案: {req_path}")
    
    # 顯示總結
    print("\n=== 安裝摘要 ===")
    print(f"成功安裝: {len(installed)} 個套件")
    if failed:
        print(f"安裝失敗: {len(failed)} 個套件")
        print(f"失敗清單: {', '.join(failed)}")
        print("請手動安裝這些套件")

if __name__ == "__main__":
    main()