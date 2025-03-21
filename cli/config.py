import configparser
import os

# Create a ConfigParser object
ini_config = configparser.ConfigParser()


# Read the INI file
ini_config.read(f"{os.getcwd()}/cli.ini")
