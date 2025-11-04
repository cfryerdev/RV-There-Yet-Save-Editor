#!/usr/bin/env python3
"""
Interactive Save Game Editor for Ride (RideGamejam)
This script allows you to edit your save file values easily.
"""

import struct
import shutil
import os
import glob

def read_int32(data, offset):
    """Read a 32-bit integer from the data."""
    return struct.unpack_from('<I', data, offset)[0]

def write_int32(data, offset, value):
    """Write a 32-bit integer to the data."""
    data_list = bytearray(data)
    struct.pack_into('<I', data_list, offset, value)
    return bytes(data_list)

def backup_file(filename):
    """Create a backup of the original file."""
    backup_dir = os.path.dirname(filename)
    backup_name = os.path.join(backup_dir, os.path.basename(filename) + '.backup')
    shutil.copy2(filename, backup_name)
    return backup_name

def list_save_files(directory='/saves'):
    """List all .sav files in the specified directory."""
    if not os.path.exists(directory):
        print(f"⚠️  Directory '{directory}' does not exist!")
        return []

    # Look for .sav files, excluding backups and meta files
    save_files = []
    for file in glob.glob(os.path.join(directory, '*.sav')):
        # Skip backup and meta files
        if not file.endswith('.backup') and not file.endswith('.meta.sav'):
            save_files.append(file)

    return sorted(save_files)

def display_save_info(filepath):
    """Display basic info about a save file."""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()

        # Check if it's a valid GVAS file
        if data[:4].decode('ascii', errors='ignore') != 'GVAS':
            return None

        # Try to read key values
        info = {
            'size': len(data),
            'checkpoint': None,
            'pens': None,
            'parts': None
        }

        # Try to read values (may fail if offsets are different)
        try:
            info['checkpoint'] = struct.unpack_from('<I', data, 0x0735)[0]
            info['pens'] = struct.unpack_from('<I', data, 0x0C8E)[0]
            info['parts'] = struct.unpack_from('<I', data, 0x0CBC)[0]
        except:
            pass

        return info
    except:
        return None

def select_save_file():
    """Interactive save file selection."""
    print("="*70)
    print("SAVE FILE SELECTION")
    print("="*70)
    print()

    save_files = list_save_files()

    if not save_files:
        print("No save files found in /saves directory!")
        print()
        print("Falling back to default location...")
        # Try the uploads directory as fallback
        fallback_files = list_save_files('/home/cfryerdev/GIT/rv-save-editor/saves/')
        if fallback_files:
            save_files = fallback_files
            print(f"Found {len(save_files)} save file(s) in /home/cfryerdev/GIT/rv-save-editor/saves/")
        else:
            print("No save files found in fallback location either.")
            return None

    if len(save_files) == 0:
        return None

    print(f"Found {len(save_files)} save file(s):\n")

    for i, filepath in enumerate(save_files, 1):
        filename = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)

        print(f"{i}. {filename}")
        print(f"   Path: {filepath}")
        print(f"   Size: {file_size:,} bytes")

        # Display save info if available
        info = display_save_info(filepath)
        if info:
            if info['checkpoint'] is not None:
                print(f"   Checkpoint: {info['checkpoint']}")
            if info['pens'] is not None:
                print(f"   EpicPens: {info['pens']}")
            if info['parts'] is not None:
                print(f"   VehicleParts: {info['parts']}")
        print()

    # Get user selection
    while True:
        try:
            choice = input(f"Select save file (1-{len(save_files)}) or 'q' to quit: ").strip()

            if choice.lower() == 'q':
                return None

            choice_num = int(choice)
            if 1 <= choice_num <= len(save_files):
                selected_file = save_files[choice_num - 1]
                print(f"\n✓ Selected: {os.path.basename(selected_file)}")
                print()
                return selected_file
            else:
                print(f"Please enter a number between 1 and {len(save_files)}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")
        except KeyboardInterrupt:
            print("\n\nCancelled by user.")
            return None

def edit_save_file(input_file, output_file, modifications):
    """
    Edit the save file with specified modifications.

    Args:
        input_file: Path to input save file
        output_file: Path to output save file
        modifications: Dict of {offset: new_value}
    """
    # Read the file
    with open(input_file, 'rb') as f:
        data = f.read()

    # Make a backup
    backup_name = backup_file(input_file)
    print(f"✓ Backup created: {backup_name}")

    # Apply modifications
    for offset, new_value in modifications.items():
        old_value = read_int32(data, offset)
        data = write_int32(data, offset, new_value)
        print(f"✓ Modified offset 0x{offset:04X}: {old_value} → {new_value}")

    # Save the modified file
    with open(output_file, 'wb') as f:
        f.write(data)

    print(f"✓ Modified save written to: {output_file}")
    print()
    print("SUCCESS! Your save file has been edited.")
    print("Replace your original save file with the modified one to use it in game.")

# Define the known offsets for this save file
OFFSETS = {
    'CurrentCheckpoint': 0x0735,
    'EpicPens': 0x0C8E,
    'VehicleParts': 0x0CBC,
    'VehicleDamage_Frame': 0x085B,
    'VehicleDamage_Engine': 0x0925,
    'VehicleDamage_TireRL': 0x09F0,
    'VehicleDamage_TireFR': 0x0ABB,
    'VehicleDamage_TireRR': 0x0B86,
    'VehicleDamage_TireFL': 0x0C51,
}

# Example usage scenarios
def example_max_currency(input_file, output_file):
    """Example: Give yourself maximum currency."""
    modifications = {
        OFFSETS['EpicPens']: 9999,
    }
    edit_save_file(input_file, output_file, modifications)

def example_max_parts(input_file, output_file):
    """Example: Give yourself maximum vehicle parts."""
    modifications = {
        OFFSETS['VehicleParts']: 9999,
    }
    edit_save_file(input_file, output_file, modifications)

def example_repair_vehicle(input_file, output_file):
    """Example: Fully repair your vehicle (set all damage to 0)."""
    modifications = {
        OFFSETS['VehicleDamage_Frame']: 0,
        OFFSETS['VehicleDamage_Engine']: 0,
        OFFSETS['VehicleDamage_TireRL']: 0,
        OFFSETS['VehicleDamage_TireFR']: 0,
        OFFSETS['VehicleDamage_TireRR']: 0,
        OFFSETS['VehicleDamage_TireFL']: 0,
    }
    edit_save_file(input_file, output_file, modifications)

def example_reset_progress(input_file, output_file):
    """Example: Reset progress to checkpoint 0."""
    modifications = {
        OFFSETS['CurrentCheckpoint']: 0,
    }
    edit_save_file(input_file, output_file, modifications)

def example_god_mode(input_file, output_file):
    """Example: God mode - max currency, max parts, full repair."""
    modifications = {
        OFFSETS['EpicPens']: 9999,
        OFFSETS['VehicleParts']: 9999,
        OFFSETS['VehicleDamage_Frame']: 0,
        OFFSETS['VehicleDamage_Engine']: 0,
        OFFSETS['VehicleDamage_TireRL']: 0,
        OFFSETS['VehicleDamage_TireFR']: 0,
        OFFSETS['VehicleDamage_TireRR']: 0,
        OFFSETS['VehicleDamage_TireFL']: 0,
    }
    edit_save_file(input_file, output_file, modifications)

def example_set_checkpoint(input_file, output_file, checkpoint_value):
    """Example: Set progress to a specific checkpoint (1-12)."""
    if not (1 <= checkpoint_value <= 12):
        print(f"⚠️  Warning: Checkpoint value {checkpoint_value} is outside typical range (1-12)")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return

    modifications = {
        OFFSETS['CurrentCheckpoint']: checkpoint_value,
    }
    edit_save_file(input_file, output_file, modifications)

if __name__ == "__main__":
    print("="*70)
    print("RIDE SAVE GAME EDITOR - Interactive Editor")
    print("="*70)
    print()

    import sys

    # Step 1: Select save file
    selected_save = select_save_file()

    if selected_save is None:
        print("No save file selected. Exiting.")
        sys.exit(0)

    # Update the input file for all examples
    global INPUT_FILE, OUTPUT_DIR
    INPUT_FILE = selected_save
    OUTPUT_DIR = os.path.dirname(selected_save)

    # If in /saves, output to /saves/modified, otherwise output to /outputs
    if '/saves' in selected_save:
        modified_dir = '/saves/modified'
        if not os.path.exists(modified_dir):
            try:
                os.makedirs(modified_dir)
            except:
                modified_dir = OUTPUT_DIR
        OUTPUT_DIR = modified_dir
    else:
        OUTPUT_DIR = '/mnt/user-data/outputs'

    print("="*70)

    # Step 2: Select modification type
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        print("Available modifications:")
        print("  1. Max Currency (9999 EpicPens)")
        print("  2. Max Vehicle Parts (9999)")
        print("  3. Repair Vehicle (all damage = 0)")
        print("  4. Reset Progress (checkpoint 0)")
        print("  5. God Mode (max everything + full repair)")
        print("  6. Set Progress Checkpoint (custom value 1-12)")
        print()
        choice = input("Enter your choice (1-6): ").strip()

    print()

    # Generate output filename
    base_name = os.path.splitext(os.path.basename(INPUT_FILE))[0]

    try:
        if choice == '1':
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_MaxCurrency.sav")
            example_max_currency(INPUT_FILE, output_file)
        elif choice == '2':
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_MaxParts.sav")
            example_max_parts(INPUT_FILE, output_file)
        elif choice == '3':
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_Repaired.sav")
            example_repair_vehicle(INPUT_FILE, output_file)
        elif choice == '4':
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_ResetProgress.sav")
            example_reset_progress(INPUT_FILE, output_file)
        elif choice == '5':
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_GodMode.sav")
            example_god_mode(INPUT_FILE, output_file)
        elif choice == '6':
            # Prompt for checkpoint value
            while True:
                try:
                    checkpoint_input = input("Enter checkpoint value (1-12): ").strip()
                    checkpoint_value = int(checkpoint_input)
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")

            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_Checkpoint{checkpoint_value}.sav")
            example_set_checkpoint(INPUT_FILE, output_file, checkpoint_value)
        else:
            print(f"Invalid choice: {choice}")
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
