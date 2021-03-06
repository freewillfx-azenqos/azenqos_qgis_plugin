import subprocess
import os
import sys

import qt_utils

def get_module_path():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_local_fp(fn):
    return os.path.join(get_module_path(), fn)

def check_and_install_requirements():
    needs_install = False

    # pkg_list = [x.strip() for x in pkg_list]
    wheel_dp = get_local_fp('wheel')
    assert os.path.isdir(wheel_dp)
    cp_pattern = f"cp{sys.version_info.major}{sys.version_info.minor}"
    compat_wheel_pattern = f"*-*-{cp_pattern}*.whl"
    
    import glob
    whl_list = glob.glob(os.path.join(wheel_dp, compat_wheel_pattern))
    whl_list = sorted(whl_list) #install numpy before scipy

    requirement_fp = get_local_fp('requirements.txt')
    requirement_list = None
    with open(requirement_fp,"r") as f:
        requirement_list = f.read().splitlines()
    for requirement in requirement_list:
        requirement = requirement.lower().strip()
        sub_index = requirement.index('==')
        lib_name = requirement[0:sub_index]
        version = requirement[sub_index+2:]
        try:
            exec("import {}".format(lib_name))
            existing_version = eval("{}.__version__".format(lib_name))
            if version != existing_version:
                raise Exception
        except:
            needs_install = True
            print("not found:", requirement)
            break

    if needs_install:
        print("need_to_restart")
        for whl in whl_list:
            subprocess.call(['python', '-m', 'pip', 'install', whl])
        try:
            subprocess.check_output(['python', '-m', 'pip', 'install', '-r', requirement_fp], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            outstr = e.output
            qt_utils.msgbox("Azenqos plugin failed to install required dependencies, please email below error msg to support@azenqos.com:\n\n" + outstr.decode("utf-8"), title="AZENQOS Dependency Install Fail")
            return False 

    return True