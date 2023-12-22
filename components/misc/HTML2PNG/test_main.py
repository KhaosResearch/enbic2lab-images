import pytest
import os
from tempfile import TemporaryDirectory
from PIL import Image

from main import html2png

# Define test data and file paths
test_data = """<!DOCTYPE html>
<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
<body>

<h2>HTML Table</h2>

<table>
  <tr>
    <th>Company</th>
    <th>Contact</th>
    <th>Country</th>
  </tr>
  <tr>
    <td>Alfreds Futterkiste</td>
    <td>Maria Anders</td>
    <td>Germany</td>
  </tr>
  <tr>
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
  <tr>
    <td>Ernst Handel</td>
    <td>Roland Mendel</td>
    <td>Austria</td>
  </tr>
  <tr>
    <td>Island Trading</td>
    <td>Helen Bennett</td>
    <td>UK</td>
  </tr>
  <tr>
    <td>Laughing Bacchus Winecellars</td>
    <td>Yoshi Tannamuri</td>
    <td>Canada</td>
  </tr>
  <tr>
    <td>Magazzini Alimentari Riuniti</td>
    <td>Giovanni Rovelli</td>
    <td>Italy</td>
  </tr>
</table>

</body>
</html>"""


def test_html2pdf():
    with TemporaryDirectory() as tmp_dir:
        tmp_input_file = os.path.join(tmp_dir, "test_input.html")
        tmp_output_file = os.path.join(tmp_dir, "test_output.png")

        # Write test data to file
        with open(tmp_input_file, "w") as file:
            file.write(test_data)

        html2png(filepath=tmp_input_file, output=tmp_output_file)

        # Check if the output file exists
        assert os.path.exists(tmp_output_file)
        assert os.path.isfile(tmp_output_file)
        assert os.path.getsize(tmp_output_file) > 0
        assert tmp_output_file.endswith(".png")


if __name__ == "__main__":
    pytest.main()
