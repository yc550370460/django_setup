import os
import ConfigParser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONF_FILE = os.path.join(os.path.dirname(CURRENT_DIR), "conf", "conf.ini")


def create_env(path, name):
    """
    :param path: env location
    :param name: env name
    :return: None if success, Exception if failed

    virtualenv [name]
    """
    cmd = "cd " + path + "&& virtualenv " + name
    result = os.system(cmd)
    if result == 0:
        print "Create env successfully"
        return True
    else:
        raise Exception("Create env failed")


def setup_django(path, version):
    """
    :param path: env path
    :param version: django version
    :return: None if success, Exception if failed

    pip install django==[version] -i https://pypi.douban.com/simple/
    """
    pip_cmd = os.path.join(path, "bin", "pip ") + "install django==" + version + " -i https://pypi.douban.com/simple/"
    resp = os.system(pip_cmd)
    print resp
    if resp == 0:
        print "Setup django successfully"
    else:
        raise Exception("Setup django failed, pip failed")


def create_django_project(path, dir, project, app):
    """
    :param dir_path: django file location
    :param project: project name
    :param app: app name
    :return: None if success, Exception if failed

    django-admin.py startproject [project]
    python manage.py startapp [app]
    """
    dir_path = os.path.join(path, dir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    cmd = "cd " + dir_path + "&&" + os.path.join(path, "bin", "django-admin.py") + " startproject " + project
    result = os.system(cmd)
    if result == 0:
        print "Create django project successfully"
        _path = dir_path + "/" + project
        cmd_app = "cd " + _path + " && " + os.path.join(path, "bin", "python") + " manage.py startapp " + app
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
            django_status = ini.get("django", "status")
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
            if django_status == "yes":
                setup_django(os.path.join(env_path, env_name), django_version)
                create_django_project(os.path.join(env_path, env_name), django_dir, django_project, django_app)
                print "Create django project and app successfully"
            else:
                if not os.path.exists(os.path.join(env_path, env_name, django_dir)):
                    os.mkdir(os.path.join(env_path, env_name, django_dir))
                print "Create non-django project successfully"
        except Exception, e:
            raise e
    else:
        raise Exception("Error: ini conf error, section error")


