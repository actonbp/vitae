# Academic CV Builder

A professional academic CV builder using Quarto, designed for tenure-track positions at R1 business schools. This repository provides a flexible, maintainable approach to creating and updating your academic CV.

## Features

- Single source of truth for all CV data using YAML files
- Multiple output formats (PDF, HTML, Word) using Quarto
- Modular structure for easy updates and maintenance
- Professional templates designed for academic tenure track positions
- Optional automation scripts for publication data

## Repository Structure

- `data/`: Contains YAML files with CV information
- `scripts/`: Contains utility scripts for managing CV data
- `templates/`: Contains Quarto templates for CV generation
- `static/`: Contains static files like images
- `output/`: Contains generated CV files
- `sources/`: Contains source documents for importing data (e.g., old CV PDFs)

## Importing Data from Existing CV

To import presentations and other data from an existing CV:

1. Place your old CV PDF in the `sources/` directory
2. Activate the Python virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Run the extraction script:
   ```bash
   ./scripts/extract_cv.py
   ```
4. When prompted, enter the path to your PDF (e.g., `sources/old_cv.pdf`)
5. Review and edit the extracted data in the generated YAML files

## Setup

1. Install Dependencies:
   - Install [Quarto](https://quarto.org/docs/get-started/)
   - Install [R](https://www.r-project.org/) or [Python](https://www.python.org/)
   - Required R packages: yaml, vitae, scholar (optional)

2. Configure Your Data:
   - Update YAML files in the `data/` directory with your information
   - Follow the provided example formats

3. Generate Your CV:
   ```bash
   ./build.sh
   ```

## Customization

- Edit Quarto templates in `templates/` to modify the CV format
- Adjust YAML structure in `data/` to match your needs
- Modify build scripts to customize the build process

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use and modify for your own needs.
