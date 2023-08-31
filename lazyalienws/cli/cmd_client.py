import zipfile, json, os, re
from lazyalienws.constants.client_constants import PLUGIN_METADATA

def create_client_file():
    create_file()
    remove_file()

def create_file():
    try:
        with zipfile.ZipFile('LazyAlienWS-client-v{}.mcdr'.format(PLUGIN_METADATA["version"]),'w') as zipobj:
            zipobj.writestr("mcdreforged.plugin.json",json.dumps(PLUGIN_METADATA, indent=4, sort_keys=True, ensure_ascii=False))
            zipobj.writestr("lazyalienws_client/__init__.py","from lazyalienws.client.mcdr_plugin import *")
            zipobj.close()
        print("Successfully create mcdr plugin")
    except Exception as e:
        print("Failed to create mcdr plugin. {}".format(e))

def remove_file():
    try:
        file = None
        for path in os.listdir("."):
            # check if current path is a file
            if os.path.isfile(path):
                re_result = re.fullmatch(r"LazyAlienWS-client-v([0-9.]+[0-9]).mcdr",path)
                if re_result and is_latest_version(PLUGIN_METADATA["version"],compared_version = re_result.groups()[0]):
                    file = path
                    os.remove(path)
                    print("Removed old plugin")
    except Exception as e:
        if file:
            print("Failed to remove old plugin automatically, plz remove '{}' manually. Error: {}".format(file, e))
        else:
            print("Failed to check version. {}".format(e))

def is_latest_version(new_version, compared_version):
	version1, version2 = new_version.split("."), compared_version.split(".")
	for v1, v2 in zip(version1, version2):
		v1, v2 = int(v1), int(v2)
		if v1 > v2:
			return True
		elif v1 < v2:
			return False
	if len(version1) == len(version2):
		return None
	else:
		return len(version1) > len(version2)