import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent


DEPLOY_DIR = PROJECT_ROOT.joinpath('deploy')
