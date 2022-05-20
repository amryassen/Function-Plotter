import pytest
import GUI.gui


@pytest.fixture
def app(qtbot):
    test_app = GUI.gui.Plotter()
    qtbot.addWidget(test_app)
    return test_app

@pytest.fixture(scope='function', autouse=True)
def first_app(app, request):
    request.instance.app = app


class Test_function:
     def x_here_or_not(self, request):
        assert request.instance.app.fn.text() == "x"
    
     def test_dialog_min_error(self, request):
        request.instance.app.min.setValue(request.instance.app.max.value())
        assert request.instance.app.error_msg.isHidden() == False
