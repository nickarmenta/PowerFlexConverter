import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_parameters_from_pf5(input_file: Path) -> dict:
    """
    Extract parameters from .pf5 file into a dictionary
    
    Args:
        input_file (Path): Path to input .pf5 file
        
    Returns:
        dict: Dictionary of parameter instances and their values
    """
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    parameters = {}
    for param in root.findall(".//Parameter"):
        instance = int(param.get("Instance"))
        value = param.text
        parameters[instance] = value
    
    return parameters

def update_frc2_parameters(input_file: Path, output_file: Path, new_params: dict) -> None:
    """
    Update specific parameters in .frc2 file
    
    Args:
        input_file (Path): Path to input .frc2 file
        output_file (Path): Path to output .frc2 file
        new_params (dict): Dictionary of parameters to update
    """
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Find the SettingValues element
    setting_values = root.find(".//SettingValues")
    if setting_values is None:
        raise ValueError("Could not find SettingValues in .frc2 file")
    
    # Parse current parameters
    current_params = {}
    param_text = setting_values.text
    param_pairs = param_text.split(';')
    for pair in param_pairs:
        if ',' in pair:
            param_num, value = pair.split(',')
            current_params[int(param_num)] = value
    
    # Update parameters 31-43 if they exist in new_params
    for param_num in range(31, 44):
        if param_num in new_params:
            current_params[param_num] = new_params[param_num]
    
    # Convert back to string format
    new_param_text = ';'.join(f"{k},{v}" for k, v in sorted(current_params.items()))
    setting_values.text = new_param_text
    
    # Write the modified XML
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def convert_pf5_to_frc2(input_file: Path, output_file: Path) -> None:
    """
    Convert a .pf5 XML file to .frc2 XML format
    
    Args:
        input_file (Path): Path to input .pf5 file
        output_file (Path): Path to output .frc2 file
    """
    try:
        # Extract parameters from .pf5 file
        new_params = extract_parameters_from_pf5(input_file)
        
        # Create a copy of the template .frc2 file and update it
        update_frc2_parameters(output_file.with_suffix('.template.frc2'), output_file, new_params)
        
        print(f"Successfully converted {input_file} to {output_file}")
        
    except ET.ParseError:
        print(f"Error: Could not parse {input_file} as XML")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert PathFinder5 (.pf5) files to FRC2 format"
    )
    
    parser.add_argument(
        'input_file',
        type=Path,
        help='Input .pf5 file path'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output .frc2 file path (optional)'
    )
    
    parser.add_argument(
        '-t', '--template',
        type=Path,
        required=True,
        help='Template .frc2 file path'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not args.input_file.exists():
        print(f"Error: Input file {args.input_file} does not exist")
        return
    
    if args.input_file.suffix.lower() != '.pf5':
        print(f"Error: Input file must have .pf5 extension")
        return
    
    if not args.template.exists():
        print(f"Error: Template file {args.template} does not exist")
        return
    
    # Generate output path if not specified
    output_file = args.output if args.output else args.input_file.with_suffix('.frc2')
    
    # Copy template to working file
    import shutil
    shutil.copy2(args.template, output_file.with_suffix('.template.frc2'))
    
    convert_pf5_to_frc2(args.input_file, output_file)

if __name__ == '__main__':
    main()