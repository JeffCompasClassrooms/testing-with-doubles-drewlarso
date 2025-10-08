import os
import pytest
from mydb import MyDB
from unittest.mock import call

todo = pytest.mark.skip(reason='todo: pending spec')


def describe_MyDB():

    @pytest.fixture(autouse=True, scope="session")
    def verify_filesystem_is_not_touched():
        yield
        assert not os.path.isfile("mydatabase.db")

    def describe_init():
        def it_assigns_fname_attribute(mocker):
            mocker.patch("os.path.isfile", return_value=True)
            db = MyDB("mydatabase.db")
            assert db.fname == "mydatabase.db"

        def it_creates_empty_database_if_it_does_not_exist(mocker):
            # set up stubs & mocks first
            mock_isfile = mocker.patch("os.path.isfile", return_value=False)
            mock_open = mocker.patch("builtins.open", mocker.mock_open())
            mock_dump = mocker.patch("pickle.dump")

            # execute on the test subject
            db = MyDB("mydatabase.db")

            # assert what happened
            mock_isfile.assert_called_once_with("mydatabase.db")
            mock_open.assert_called_once_with("mydatabase.db", "wb")
            mock_dump.assert_called_once_with([], mock_open.return_value)

        def it_does_not_create_database_if_it_already_exists(mocker):
            mock_isfile = mocker.patch("os.path.isfile", return_value=True)
            mock_open = mocker.patch("builtins.open", mocker.mock_open())
            mock_dump = mocker.patch("pickle.dump")

            db = MyDB("mydatabase.db")

            mock_isfile.assert_called_once_with("mydatabase.db")
            mock_open.assert_not_called()
            mock_dump.assert_not_called()

    def describe_loadStrings():
        def it_loads_an_array_from_a_file_and_returns_it(mocker):
            mock_isfile = mocker.patch("os.path.isfile", return_value=True)
            mock_open = mocker.patch("builtins.open", mocker.mock_open())
            mock_load = mocker.patch(
                "pickle.load", return_value=["hello", "world"])

            db = MyDB("mydatabase.db")
            arr = db.loadStrings()

            mock_open.assert_called_once_with("mydatabase.db", "rb")
            mock_load.assert_called_once()
            assert arr == ["hello", "world"]

        def it_raises_an_error_when_loading_from_a_nonexisting_file(mocker):
            mock_isfile = mocker.patch("os.path.isfile", return_value=True)
            mock_open = mocker.patch(
                "builtins.open", side_effect=FileNotFoundError)
            mock_load = mocker.patch(
                "pickle.load", return_value=["hello", "world"])

            db = MyDB("mydatabase.db")
            with pytest.raises(FileNotFoundError):
                db.loadStrings()

            mock_open.assert_called_once()
            mock_load.assert_not_called()

    def describe_saveStrings():
        def it_saves_the_given_array_to_a_file(mocker):
            mock_isfile = mocker.patch("os.path.isfile", return_value=True)
            mock_open = mocker.patch("builtins.open", mocker.mock_open())
            mock_dump = mocker.patch("pickle.dump")

            db = MyDB("mydatabase.db")
            db.saveStrings(["hello", "world"])

            mock_open.assert_called_once_with("mydatabase.db", "wb")
            mock_dump.assert_called_once_with(
                ["hello", "world"], mock_open.return_value)

        def it_raises_an_error_when_saving_strings_to_a_nonexistent_file(mocker):
            mock_isfile = mocker.patch("os.path.isfile", return_value=True)
            mock_open = mocker.patch(
                "builtins.open", side_effect=FileNotFoundError)
            mock_dump = mocker.patch("pickle.dump")

            db = MyDB("mydatabase.db")
            with pytest.raises(FileNotFoundError):
                db.saveStrings(["hello", "world"])

            mock_open.assert_called_once_with("mydatabase.db", "wb")
            mock_dump.assert_not_called()

    def describe_saveString():
        def it_appends_string_element_to_existing_database(mocker):
            mock_isfile = mocker.patch("os.path.isfile", return_value=True)
            mock_open = mocker.patch("builtins.open", mocker.mock_open())
            mock_load_strings = mocker.patch(
                "mydb.MyDB.loadStrings", return_value=["hello", "world"])
            mock_save_strings = mocker.patch("mydb.MyDB.saveStrings")

            db = MyDB("mydatabase.db")
            db.saveString("python")

            mock_load_strings.assert_called_once()
            mock_save_strings.assert_called_once_with(
                ["hello", "world", "python"])

        def it_appends_number_element_to_existing_database(mocker):
            mock_isfile = mocker.patch("os.path.isfile", return_value=True)
            mock_open = mocker.patch("builtins.open", mocker.mock_open())
            mock_load_strings = mocker.patch(
                "mydb.MyDB.loadStrings", return_value=["hello", "world"])
            mock_save_strings = mocker.patch("mydb.MyDB.saveStrings")

            db = MyDB("mydatabase.db")
            db.saveString(47)

            mock_load_strings.assert_called_once()
            mock_save_strings.assert_called_once_with(
                ["hello", "world", 47])

        def it_appends_object_element_to_existing_database(mocker):
            mock_isfile = mocker.patch("os.path.isfile", return_value=True)
            mock_open = mocker.patch("builtins.open", mocker.mock_open())
            mock_load_strings = mocker.patch(
                "mydb.MyDB.loadStrings", return_value=["hello", "world"])
            mock_save_strings = mocker.patch("mydb.MyDB.saveStrings")

            class Squirrel:
                def __init__(self, name, size):
                    self.name = name
                    self.size = size

            db = MyDB("mydatabase.db")
            squirrel = Squirrel("Charles", "Medium")
            db.saveString(squirrel)

            mock_load_strings.assert_called_once()
            mock_save_strings.assert_called_once_with(
                ["hello", "world", squirrel])
