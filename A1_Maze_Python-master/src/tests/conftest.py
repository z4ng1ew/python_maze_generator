import pytest

from modules.load import Loader


@pytest.fixture(scope='session')
def maze1():
    loader: Loader = Loader()
    loader.download('files/1.txt')
    yield loader.maze
