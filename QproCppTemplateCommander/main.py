from QuickProject.Commander import Commander
from . import *


app = Commander(name)


@app.command()
def compile(debug: bool = False):
    """
    🔨 编译
    """
    # * 你可以在此函数的参数中添加你需要的define, bool类型参数将自动转换为-D <参数名>，其他类型参数将自动转换为-D <参数名>=<参数值>。因此推荐为bool类型参数设置默认值为False。
    # ! 不支持list类型参数
    include = " ".join([f"-I {path}" for path in includePath])
    source = " ".join([f"{path}" for path in sourcePath])
    lib_path = " ".join([f"-L {path}" for path in libPath])
    libs = " ".join([f"-l{lib}" for lib in usingLib])
    others = " ".join(other_flags)

    defines = []
    cur_func_fig = app.fig_table[2]

    for item in cur_func_fig["args"]:
        _name = item["name"]
        defines.append(f"-D {name}='{eval(_name)}'")
    for item in cur_func_fig["options"]:
        _name = item["name"].strip("-")
        if "args" not in item and eval(_name):
            defines.append(f"-D {_name.upper()}")
        elif "args" in item:
            defines.append(f"-D {_name}='{eval(_name)}'")
    defines = " ".join(defines)

    external_exec(
        f"{cc} -std={standard} -O{optimization} {include + ' ' if include else ''}{lib_path + ' ' if lib_path else ''}{source + ' ' if source else ''}{defines + ' ' if defines else ''}{libs + ' ' if libs else ''}{others + ' ' if others else ''}-o dist/{name}"
    )


@app.command()
def run():
    """
    🏃 运行
    """
    external_exec(f"./dist/{name}", __expose=True)


@app.command()
def export(filepath: str, to_path: str):
    """
    ⚠️ 导出文件 (转换msg.h输出方式为printf)

    :param filepath: 源文件路径
    :param to_path: 目标文件路径
    """
    import re

    mp = {
        "info": "信息",
        "warn": "警告",
        "error": "错误",
        "success": "成功",
    }

    with open(filepath, "r") as f:
        ct = f.read()
    with open(to_path, "w") as f:
        for line in ct.splitlines():
            _line = line.strip()
            if "#include <msg.h>" == _line:
                continue
            if _line.startswith("echo"):
                # 计算缩进
                indent = len(line) - len(line.lstrip()) - 1

                args = None
                try:
                    status, fmt, args = re.findall(
                        'echo\((.*?),.*?"(.*?)",.*?(.*?)\);', _line
                    )[0]
                except IndexError:
                    status, fmt = re.findall('echo\((.*?),.*?"(.*?)"\);', _line)[0]
                if status in ["start_status", "stop_status", "split"]:
                    continue
                print(
                    " " * indent, f'printf("[{mp[status]}] {fmt}");', file=f
                ) if args is None else print(
                    " " * indent,
                    f'printf("[{mp[status]}] {fmt}", {args.strip()});',
                    file=f,
                )
            else:
                print(line, file=f)


def main():
    """
    * 注册为全局命令时, 默认采用main函数作为命令入口, 请勿将此函数用作它途.
    * When registering as a global command, default to main function as the command entry, do not use it as another way.
    """
    app()


if __name__ == "__main__":
    main()
