# PowerFlexConverter

A simple yet powerful tool that converts Allen Bradley PowerFlex (.pf5) parameter files to Mitsubishi (.frc2) format with just one command.

## Features

- 🚀 Quick and easy conversion from PowerFlex to Mitsubishi format
- ⚡ Preserves all critical parameters (31-43)
- 🛡️ Built-in error handling and validation
- 🔧 Customizable template support

## Usage

Converting files is as simple as:

```bash
python app/__main__.py -i input.pf5 -o output.frc2
```

### Arguments

- `input_file.pf5`: Your PowerFlex parameter file
- `-t, --template`: Template .frc2 file to base the conversion on
- `-o, --output`: (Optional) Custom output file path. If not specified, creates a .frc2 file in the same location as the input

### Example

```bash
python -m app drive_params.pf5 -t mitsubishi_template.frc2 -o converted_params.frc2
```

## Why PowerFlexConverter?

- **Save Time**: Convert drive parameters in seconds instead of manual reentry
- **Reduce Errors**: Eliminate manual data entry mistakes
- **Streamline Migration**: Makes transitioning from Allen Bradley to Mitsubishi drives effortless

## Requirements

- Python 3.6 or higher
- No additional dependencies required!
