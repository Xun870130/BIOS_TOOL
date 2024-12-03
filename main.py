import argparse
import ctrl_pwswitch as sw
import client_windows 
import client_java 
import res_ASCIIart 
import ctrl_dediprog 

def main():
    """
    Main program to automate BIOS programming and system installation.

    This script selects a device and installer type based on command-line arguments,
    initializes the required components, and performs the full automation process.

    Raises:
        ValueError: If an invalid IP address or installer type is provided.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Automated Installation Script",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "ip", choices=["192.168.0.213", "192.168.0.211"],
        help="Device controller IP, e.g., 192.168.0.211"
    )
    parser.add_argument(
        "type", choices=["win", "java"],
        help="Select client type: 'win' or 'java'"
    )
    args = parser.parse_args()

    ip = f"http://{args.ip}:16628"
    installer_type = args.type

    # Map BIOS paths based on IP address
    bios_map = {
        "http://192.168.0.213:16628": r"C:\__RVS_Execute_Software__\GoldenBIOS\WhiskeyLake_U\WhiskeyLake_U_3.bin",
        "http://192.168.0.211:16628": r"C:\__RVS_Execute_Software__\GoldenBIOS\IceLake_U\IceLake_U_3.bin"
    }
    bios_path = bios_map.get(ip)
    if not bios_path:
        raise ValueError(f"Unknown IP address: {ip}")

    # Map installer types
    installers = {
        "win": client_windows.AutoInstaller,
        "java": client_java.AutoInstaller
    }
    installer_class = installers.get(installer_type)
    if not installer_class:
        raise ValueError(f"Unknown installer type: {installer_type}")

    installer = installer_class(ip=ip)

    # Initialize components
    controller = sw.DeviceController(IP_adr=ip)
    ascii_art = res_ASCIIart.ASCIIArtBuilder()
    directory = r"C:\Program Files (x86)\DediProg\SF100"
    programmer = ctrl_dediprog.Programmer(directory, bios_path, ascii_art)

    try:
        # Perform automation steps
        print("Checking AC power status...")
        controller.ACoffcheck()
        print("Turning on DP module...")
        controller.dp_on()
        print("Running BIOS programming...")
        programmer.run()
        print("Turning off DP module...")
        controller.dp_off()
        print("Resetting CMOS...")
        controller.cmos_switch()
        print("Turning on AC power...")
        controller.AConcheck()
        print("Starting system installation...")
        installer.start_installation()
        print("All operations completed successfully!")

    except Exception as e:
        print(f"Error occurred during execution: {e}")
        # Additional error handling or cleanup logic can be added here

if __name__ == "__main__":
    main()
