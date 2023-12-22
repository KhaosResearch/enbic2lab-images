# EnBiC2-Lab Images Catalog

This repository contains the images used in the EnBiC2-Lab project. 

## Project structure

Project structure is as follows:

* `components/`: contains the images of the components used in the project.
* `workflows/`: JSON files representation of each workflow (ready to be imported in `dramax`).

## Schema compliance

To ensure that the components are compliant with the [proposed schema](annotation.schema.json), you can use the [check-jsonschema](https://check-jsonschema.readthedocs.io/en/latest/index.html) tool:

```bash
check-jsonschema --schemafile annotation.schema.json components/**/annotation*.json
```

## License

This project is licensed under the CC BY-NC-ND 4.0 license.

![CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png)

See [LICENSE](LICENSE) file for more details.
