import unittest
from unittest.mock import patch

from main import get_filename, main


class TestMain(unittest.TestCase):
    def test_get_filename(self):
        url = "http://example.com/file.csv"
        expected_filename = "file.csv"

        filename = get_filename(url)

        self.assertEqual(filename, expected_filename)

    def test_get_filename_from_s3_uri(self):
        url = "minio://bucket_name/file.csv"
        expected_filename = "file.csv"

        filename = get_filename(url)

        self.assertEqual(filename, expected_filename)

    def test_get_filename_from_s3_uri_long(self):
        url = "minio://bucket_name/a/b/c/d/file.csv"
        expected_filename = "file.csv"

        filename = get_filename(url)

        self.assertEqual(filename, expected_filename)

    def test_get_filename_with_query_string(self):
        url = "http://example.com/file.csv?param=value"
        expected_filename = "file.csv"

        filename = get_filename(url)

        self.assertEqual(filename, expected_filename)

    @patch("urllib.request.urlretrieve")
    def test_main_success(self, mock_urlretrieve):
        url = "http://example.com/file.csv"
        query_string = "?param=value"
        filepath = "data/new_name.csv"
        expected_output = "data/new_name.csv"

        main(url, query_string, filepath)

        mock_urlretrieve.assert_called_once_with(url + query_string, expected_output)

    def test_main_url_error(self):
        url = "non_url/file.csv"
        output_path = "data"

        with self.assertRaises(Exception):
            main(url, output_path, None)


if __name__ == "__main__":
    unittest.main()
