import os
import ConfigParser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONF_FILE = os.path.join(os.path.dirname(CURRENT_DIR), "conf", "conf.ini")


def create_env(path, name):
    cmd = "cd " + path + "&& virtualenv " + name
    result = os.system(cmd)
    if result == 0:
        print "Create env successfully"
        return True
    else:
        raise Exception("Create env failed")


def setup_django(path, version):

    pip_cmd = os.path.join(path, "bin", "pip ") + "install django==" + version + " -i https://pypi.douban.com/simple/"
    resp = os.system(pip_cmd)
    print resp
    if resp == 0:
        print "Setup django successfully"
    else:
        raise Exception("Setup django failed, pip failed")


def create_django_project(path, project, app):
    if not os.path.exists(path):
        os.makedirs(path)
    cmd = "cd " + path + "&& django-admin.py startproject " + project
    result = os.system(cmd)
    if result == 0:
        print "Create django project successfully"
        path = path + "/" + project
        cmd_app = "cd " + path + "&& python manage.py startapp " + app
        resp = os.system(cmd_app)
        if resp == 0:
            print "Create django app successfully"
        else:
            raise Exception("Error: Create app failed")
    else:
        raise Exception("Error: Create project failed")


if __name__ == "__main__":
    if not os.path.exists(CONF_FILE):
        raise Exception("Error: conf file not exist")
    ini = ConfigParser.ConfigParser()
    ini.read(CONF_FILE)
    if "env" in ini.sections() and "django" in ini.sections():
        try:
            env_path = ini.get("env", "path")
            env_name = ini.get("env", "name")
            django_dir = ini.get("django", "dir")
            django_project = ini.get("django", "project")
            django_app = ini.get("django", "app")
            django_version = ini.get("django", "version")

        except Exception, e:
            print e
            print "Error: ini conf error"
            raise Exception("Error: ini conf error")
        if not os.path.exists(env_path):
            os.makedirs(env_path)
        try:
            create_env(env_path, env_name)
            setup_django(os.path.join(env_path, env_name), django_version)
            create_django_project(os.path.join(env_path, env_name, django_dir), django_project, django_app)
            print "Create django project and app successfully"
        except Exception, e:
            raise e
    else:
        raise Exception("Error: ini conf error, section error")


