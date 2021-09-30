from PyQt5.QtWidgets import QApplication
from server_overview_widget import server_overview_widget
import analyzer_vars
import integration_test_helpers


def test():
    app = QApplication([])
    print("app: ", app)  # use it so pyflakes wont complain - we need a ref to qapplicaiton otherwise we'll get segfault
    gv = integration_test_helpers.get_global_vars(login=True)
    dw = server_overview_widget(None, gv)
    dw.show()
    result = app.exec()
    print("result: {}".format(result))


if __name__ == "__main__":
    test()
