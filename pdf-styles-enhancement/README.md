# PDF Styles Enhancement

This project aims to enhance the PDF generation capabilities by introducing various styles for creating visually appealing documents. The styles are designed to cater to different themes and preferences, making it easier for users to create customized PDFs.

## Project Structure

- **src/**: Contains the source code for the PDF styles enhancement.
  - **styles/**: Directory for different PDF styles.
    - **base_style.py**: Contains the base style class that other styles will inherit from.
    - **travel_style.py**: Implements a style specifically for travel-themed PDFs.
    - **tech_style.py**: Implements a modern, technology-oriented style.
    - **seasonal_style.py**: Implements styles that reflect seasonal themes.
    - **cinematic_style.py**: Implements a cinematic style for storytelling through PDFs.
  - **utils/**: Contains utility functions and helpers.
    - **color_utils.py**: Utility functions for color manipulation and management.
  - **main.py**: The main entry point for generating PDFs using the defined styles.

- **tests/**: Contains unit tests for the styles and utilities.
  - **test_styles.py**: Tests for verifying the functionality of different styles.

- **resources/**: Contains additional resources such as fonts.
  - **fonts/**: Directory for custom fonts used in the PDF styles.
    - **custom_fonts.txt**: A list of custom fonts available for use.

- **examples/**: Contains example scripts demonstrating the usage of different styles.
  - **style_samples.py**: Sample code showcasing how to apply various styles to PDF generation.

- **requirements.txt**: Lists the dependencies required for the project.

## Installation

To install the required packages, run:

```
pip install -r requirements.txt
```

## Usage

To generate a PDF with a specific style, modify the `main.py` file to select the desired style and provide the necessary content. You can refer to the examples in the `examples/style_samples.py` for guidance.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.