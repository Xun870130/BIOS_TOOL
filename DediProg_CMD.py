import subprocess
import os
import sys


class Programmer:
    """
    A class for managing chip detection and programming processes.
    Includes functionality to check chips, execute programming commands,
    and display results.
    """

    def __init__(self, directory: str, bios_path: str, ascii_art: callable):
        """
        Initializes the Programmer class.

        Args:
            directory (str): The execution directory for dpcmd.
            bios_path (str): The full path to the BIOS file for programming.
            ascii_art (callable): The ASCIIArtBuilder object for displaying ASCII messages.
        """
        if hasattr(sys, '_MEIPASS'):
            self.current_directory = sys._MEIPASS  # PyInstaller environment
        else:
            self.current_directory = os.getcwd()  # Standard working directory

        self.directory = directory
        self.bios_path = bios_path
        self.ascii_art = ascii_art
        self.detect_command = ["dpcmd", "-d"]
        self.program_command = ["dpcmd", "-u", self.bios_path]

    def run_command_and_check(self, command: list[str], success_keyword: str) -> bool:
        """
        Executes a command and checks if the output contains a target string.

        Args:
            command (list[str]): The command to execute as a list of strings.
            success_keyword (str): The success keyword to look for in the output.

        Returns:
            bool: True if the keyword is found, otherwise False.
        """
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=self.directory)
            success = False
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output and success_keyword in output:
                    success = True
            return success
        except Exception as e:
            print(f"Command execution failed: {e}")
            return False

    def detect_chip(self) -> bool:
        """
        Detects if a chip is present using a specific detection command.

        Returns:
            bool: True if the chip is successfully detected, otherwise False.
        """
        if self.bios_path == r"C:\__RVS_Execute_Software__\GoldenBIOS\IceLake_U\IceLake_U_3.bin":
            check = "W25Q256FV chip size is 33554432 bytes"
        elif self.bios_path == r"C:\__RVS_Execute_Software__\GoldenBIOS\WhiskeyLake_U\WhiskeyLake_U_3.bin":
            check = "W25Q256FV chip size is 0x02000000 bytes"
        else:
            check = ""  # No matching BIOS file
        print("Detecting chip...")
        return self.run_command_and_check(self.detect_command, check)

    def program_chip(self) -> bool:
        """
        Executes the chip programming process.

        Returns:
            bool: True if the programming is successful, otherwise False.
        """
        print(self.ascii_art.call("programing"))
        return self.run_command_and_check(self.program_command, "Automatic program OK")

    def run(self):
        """
        The main entry point:
        Executes chip detection and programming and displays corresponding ASCII messages.
        """
        if self.detect_chip():
            if self.program_chip():
                print(self.ascii_art.call("success"))
            else:
                print("Failed: Programming failed")
        else:
            print(self.ascii_art.call("error"))
