import azq_utils
from PyQt5.QtCore import  QDateTime

def test():
    ts0 = azq_utils.datetimeStringtoTimestamp("2021-04-22 15:22:18.000")
    print("ts: {}".format(ts0))
    ts1 = azq_utils.datetimeStringtoTimestamp("2021-04-22 15:22:18")
    print("ts: {}".format(ts1))
    assert ts0 is not None
    assert abs(ts0 - ts1) < 0.1
    qdatetime = QDateTime.fromString("2021-04-22 15:22:18.000", "yyyy-MM-dd hh:mm:ss.z")
    qdatetime = azq_utils.datetimeStringtoTimestamp(qdatetime)
    assert qdatetime == ts0

if __name__ == "__main__":
    test()
