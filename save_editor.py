#!/usr/bin/env python3
"""
Save Game Editor for Unreal Engine GVAS files
Game: Ride (RideGamejam)
"""

import struct
import sys

def find_property_value(data, property_name, property_type='IntProperty'):
    """Find a property and its value in the save file."""
    prop_bytes = property_name.encode('ascii') + b'\x00'
    pos = data.find(prop_bytes)

    if pos == -1:
        return None, None

    # Skip property name and find the value
    # Typical structure: PropertyName + PropertyType + metadata + value
    # For IntProperty, value is typically ~25-30 bytes after property name

    offset_attempts = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
    for offset_delta in offset_attempts:
        value_offset = pos + len(prop_bytes) + offset_delta
        if value_offset + 4 <= len(data):
            try:
                value = struct.unpack_from('<I', data, value_offset)[0]
                # Check if this looks like a reasonable value (not 0 or too large)
                if 0 <= value < 1000000:
                    return value_offset, value
            except:
                continue

    return None, None

def analyze_save_file(filename):
    """Analyze the save file and display key information."""
    with open(filename, 'rb') as f:
        data = f.read()

    print("="*70)
    print(f"SAVE FILE ANALYSIS: {filename}")
    print("="*70)
    print(f"File Size: {len(data)} bytes")
    print(f"Magic: {data[:4].decode('ascii')}")
    print()

    # Find and display key properties
    properties = [
        ('CurrentCheckpoint', 'Current checkpoint progress'),
        ('EpicPens', 'Currency/collectible count'),
        ('VehicleParts', 'Vehicle parts count'),
    ]

    print("KEY VALUES:")
    print("-" * 70)
    results = {}

    for prop_name, description in properties:
        offset, value = find_property_value(data, prop_name)
        if offset:
            print(f"{prop_name:20s} @ 0x{offset:04X}  = {value:10d}  ({description})")
            results[prop_name] = (offset, value)
        else:
            print(f"{prop_name:20s} - NOT FOUND")

    print()

    # Look for vehicle damage values
    print("VEHICLE DAMAGE:")
    print("-" * 70)
    damage_types = ['Frame', 'Engine', 'Tire.RL', 'Tire.FR', 'Tire.RR', 'Tire.FL']
    for damage_type in damage_types:
        search_str = f'DamageType.{damage_type}'
        pos = data.find(search_str.encode('ascii'))
        if pos != -1:
            # Value is typically ~30-40 bytes after the damage type name
            for offset_delta in range(30, 50):
                value_offset = pos + len(search_str) + offset_delta
                if value_offset + 4 <= len(data):
                    try:
                        value = struct.unpack_from('<I', data, value_offset)[0]
                        if 0 <= value <= 100:  # Damage is typically 0-100
                            print(f"  {damage_type:15s} @ 0x{value_offset:04X}  = {value:3d}")
                            break
                    except:
                        continue

    print()
    print("="*70)
    print()

    return data, results

def edit_value(data, offset, new_value):
    """Edit a 32-bit integer value in the save file."""
    data_list = bytearray(data)
    struct.pack_into('<I', data_list, offset, new_value)
    return bytes(data_list)

def save_modified_file(data, output_filename):
    """Save the modified data to a new file."""
    with open(output_filename, 'wb') as f:
        f.write(data)
    print(f"✓ Modified save written to: {output_filename}")

# Main execution
if __name__ == "__main__":
    input_file = '/saves/TimNPeans.sav'

    # Analyze the file
    data, properties = analyze_save_file(input_file)

    print("EDITING OPTIONS:")
    print("="*70)
    print("This save file contains the following editable values:")
    print()

    for prop_name, (offset, value) in properties.items():
        print(f"  • {prop_name}: Current = {value}, Offset = 0x{offset:04X}")

    print()
    print("You can modify these values by:")
    print("  1. Using the hex offset to manually edit with a hex editor")
    print("  2. Using this Python script to programmatically change values")
    print()
    print("Example edits to try:")
    print("  - CurrentCheckpoint: Set to 0 to restart from beginning")
    print("  - EpicPens: Increase to give yourself more currency")
    print("  - VehicleParts: Increase available parts")
    print()
    print("Vehicle damage values can also be edited (set to 0 for no damage)")
