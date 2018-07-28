from napari.gui.base._util import (is_qt_class, is_qt_func, is_qt_prop,
                                   qt_getter_to_setter, get_class_doc,
                                   get_func_doc, get_prop_doc, get_meth_doc,
                                   camel_to_snake)


def test_is_qt_class():
    assert is_qt_class('QApplication') == True
    assert is_qt_class('qDrawPlainRect') == False
    assert is_qt_class('Application') == False


def test_is_qt_func():
    assert is_qt_func('qDrawPlainRect') == True
    assert is_qt_func('QApplication') == False
    assert is_qt_func('quit') == False


def test_is_qt_prop():
    assert is_qt_prop('foo', ['foo', 'setFoo']) == True
    assert is_qt_prop('setFoo', ['foo', 'setFoo']) == False
    assert is_qt_prop('foo', ['foo', 'bar', 'setBar']) == False


def test_qt_getter_to_setter():
    assert qt_getter_to_setter('foo') == 'setFoo'
    assert qt_getter_to_setter('bar') == 'setBar'


def test_get_class_doc():
    assert get_class_doc('QApplication') == 'http://doc.qt.io/qt-5/QApplication.html'
    assert get_class_doc('QAbstractButton') == 'http://doc.qt.io/qt-5/QAbstractButton.html'


def test_get_func_doc():
    assert get_func_doc('qDrawPlainRect') == 'http://doc.qt.io/qt-5/qdrawutil-h.html#qDrawPlainRect'


def test_get_prop_doc():
    assert get_prop_doc('QApplication', 'keyboardInputInterval') == 'http://doc.qt.io/qt-5/QApplication.html#keyboardInputInterval-prop'


def test_get_meth_doc():
    assert get_meth_doc('QApplication', 'alert') == 'http://doc.qt.io/qt-5/QApplication.html#alert'
    assert get_meth_doc('qApp') == 'http://doc.qt.io/qt-5/QApplication.html#qApp'


def test_camel_to_snake():
    assert camel_to_snake('drawPlainRect') == 'draw_plain_rect'
