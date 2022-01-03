from dynaconf import Dynaconf

conf = Dynaconf(settings_files=["settings.yaml", ".secrets.yaml"])
