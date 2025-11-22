import os
import re
import subprocess
from collections import defaultdict
from packaging import version, specifiers

# 路径设置（根据需求修改）
COMFYUI_PLUGIN_PATH = r"D:\ComfyUI-2025-11-19\ComfyUI\custom_nodes" # ComfyUI目录路径 解释器路径
PYTHON_PATH = r"D:\ComfyUI-2025-11-19\python\python.exe"  #  ComfyUI 虚拟环境 Python 解释器路径
SITE_PACKAGES_PATH = r"D:\ComfyUI-2025-11-19\python\Lib\site-packages"  # ComfyUI 插件安装依赖路径 site-packages 路径

def parse_requirements_line(line):
    line = line.strip()
    if line.startswith("#") or not line:
        return None, None
    match = re.match(r'^([a-zA-Z0-9_\-]+)([<>=!~]+[^\s]*)?', line)
    if match:
        pkg = match.group(1).lower()
        ver = match.group(2) if match.group(2) else ""
        return pkg, ver
    return None, None


def collect_all_plugin_requirements(plugin_dir):
    all_reqs = defaultdict(list)
    for plugin in os.listdir(plugin_dir):
        plugin_path = os.path.join(plugin_dir, plugin)
        req_path = os.path.join(plugin_path, "requirements.txt")
        if os.path.isdir(plugin_path) and os.path.exists(req_path):
            with open(req_path, "r", encoding="utf-8") as f:
                for line in f:
                    pkg, ver = parse_requirements_line(line)
                    if pkg:
                        all_reqs[pkg].append((ver, plugin))
    return all_reqs


def get_installed_version(pkg_name):
    try:
        result = subprocess.run([PYTHON_PATH, "-m", "pip", "show", pkg_name], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("Version:"):
                return line.split(":", 1)[1].strip()
    except Exception:
        return None
    return None


def version_satisfies(installed_ver, required_ver):
    if not required_ver:
        return True
    try:
        spec = specifiers.SpecifierSet(required_ver)
        return version.parse(installed_ver) in spec
    except Exception:
        return True


def prompt_install_packages(package_commands):
    if not package_commands:
        print("\n无需安装缺失依赖。✅")
        return

    print("\n--- 缺失依赖安装选项 ---")
    print("[0] 安装全部缺失依赖")
    for idx, (pkg, cmd) in enumerate(package_commands.items(), start=1):
        print(f"[{idx}] 安装 {pkg:<20} 👉 {cmd}")

    user_input = input("\n请输入你要安装的编号（用英文逗号分隔，如 1,2，输入0安装全部，或直接回车跳过）： ").strip()
    if not user_input:
        print("跳过安装。❎")
        return

    try:
        choices = [int(x.strip()) for x in user_input.split(',') if x.strip().isdigit()]
        selected = list(package_commands.items())

        if 0 in choices:
            print("\n开始安装全部缺失依赖...")
            for pkg, cmd in selected:
                try:
                    print(f"\n正在安装：{pkg} ...")
                    subprocess.run(cmd.split(), check=True)
                except subprocess.CalledProcessError as e:
                    print(f"安装 {pkg} 失败，跳过。错误信息：{e}")
            print("\n全部安装尝试完毕。")
        else:
            for i in choices:
                if 1 <= i <= len(selected):
                    pkg, cmd = selected[i - 1]
                    try:
                        print(f"\n正在安装：{pkg} ...")
                        subprocess.run(cmd.split(), check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"安装 {pkg} 失败，跳过。错误信息：{e}")
                else:
                    print(f"编号 {i} 无效，跳过。")

    except Exception as e:
        print(f"安装过程中发生错误：{e}")


def check_conflicts(all_reqs):
    print("\n=== ComfyUI 插件依赖冲突检测报告 === 混沌云制作 === 2025.6.27 ")
    print("=== 需要定制LORA可以联系我 === 微信 : chaosdoor  ")
    print("=== https://www.liblib.art/userpage/52322c5d27404cd28aea54b9641d5451/publish ")
    print("=== 专注于电商落地服务 ===\n")

    summary_table = []
    install_commands = dict()
    total_plugins = set()
    total_packages = set()
    conflicts = 0
    missing = 0
    incompatible = 0

    for pkg, entries in all_reqs.items():
        total_packages.add(pkg)
        for _, p in entries:
            total_plugins.add(p)

        version_set = set(ver for ver, _ in entries if ver)
        row_notes = []

        if len(version_set) > 1:
            conflicts += 1
            print(f"[冲突] 包 '{pkg}' 被多个插件要求不同版本：")
            for ver, plugin in entries:
                print(f"  - 插件 `{plugin}` 需要 `{pkg}{ver}`")
                row_notes.append(f"冲突: {plugin} 要求 {pkg}{ver}")

        installed_ver = get_installed_version(pkg)
        if installed_ver:
            for ver, plugin in entries:
                if ver and not version_satisfies(installed_ver, ver):
                    incompatible += 1
                    print(f"[不兼容] 插件 `{plugin}` 需要 `{pkg}{ver}`，但系统安装版本为 {installed_ver}")
                    row_notes.append(f"不兼容: {plugin} 需 {ver}, 实际 {installed_ver}")
        else:
            missing += 1
            print(f"[未安装] 系统未检测到包 `{pkg}`，被以下插件需要：")
            for ver, plugin in entries:
                print(f"  - 插件 `{plugin}` 要求 `{pkg}{ver}`")
                version_hint = ver if ver else ""
                pip_command = f"{PYTHON_PATH} -m pip install {pkg}{version_hint}"
                install_commands[pkg] = pip_command
                row_notes.append(f"未安装: {plugin} 需要 {pkg}{ver}")

        if row_notes:
            summary_table.append((pkg, " ; ".join(row_notes)))

    print("\n--- 汇总表格 ---")
    print("{:<25} {:<80}".format("包名", "问题描述"))
    print("-" * 110)
    for pkg, note in summary_table:
        print("{:<25} {:<80}".format(pkg, note))

    print("\n--- 总结 ---")
    print(f"共检测插件数: {len(total_plugins)}")
    print(f"共检测依赖包数: {len(total_packages)}")
    print(f"冲突项: {conflicts}")
    print(f"未安装项: {missing}")
    print(f"不兼容项: {incompatible}")

    prompt_install_packages(install_commands)


if __name__ == "__main__":
    # 打印路径设置，确保正确
    print(f"Comfyui插件路径: {COMFYUI_PLUGIN_PATH}")
    print(f"Comfyui虚拟环境PYTHON路径: {PYTHON_PATH}")
    print(f"Comfyui虚拟环境依赖安装路径: {SITE_PACKAGES_PATH}")

    if not os.path.exists(COMFYUI_PLUGIN_PATH):
        print("[错误] custom_nodes 插件目录不存在，请检查路径是否正确。")
    else:
        reqs = collect_all_plugin_requirements(COMFYUI_PLUGIN_PATH)
        check_conflicts(reqs)
