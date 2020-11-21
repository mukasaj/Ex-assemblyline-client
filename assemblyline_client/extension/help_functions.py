"""
Filename:       help_functions.py
Description:    This file contains all of the help functions for each of the commands that can be run in the CLI
Authors:        Liam Henley-Vachon
Version:        0.0.2
Last Updated:   07/17/2020
"""


# This function displays the help menu for the alert command
def help_alert():
    pass


# This function displays the help menu for the auth command
def help_auth():
    pass


# This function displays the help menu for the bundle command
def help_bundle():
    text = """
    Create and restore submission bundles\n
    Usage:
    \tbundle <optional arguments> <sid> OR <path/to/file>\n
    Parameters:
    \t<optional arguments>      The type of bundle operation being performed
    \t<sid>                     ID of the submission to create the bundle for
    \t<path/to/file>            Location of the file to be imported\n
    Optional Arguments:
    \t-c                        Creates a bundle containing the submission results and the associated files
    \t-i                        Import a bundle file into the system\n
    Examples:
    \t# Create bundle
    \tbundle -c 2esf5...7mm9y\n
    \t# Import bundle
    \tbundle -i "/path/to/file/bundle"
    """
    print(text)


# This function displays the help menu for different commands
def help_commands():
    print("\nAssemblyline CLI commands (type 'help <topic>'):")
    print("===================================================")
    print("alert   auth     bundle     documentation  error   file       hash_search  heuristics  ingest  live  result")
    print("search  service  signature  submission     submit  sysconfig  user         webauthn    workflow\n")


# This function displays the help menu for the documentation command
def help_documentation():
    text = """
    Loop through all registered API paths and display their documentation. Returns a list of API definitions\n
    Usage:
    \tdocumentation\n
    Example:
    \t# Get API documentation
    \tdocumentation
    """
    print(text)


# This function displays the help menu for the error command
def help_error():
    pass


# This function displays the help menu for the file command
def help_file():
    text = """
    Perform operations on files\n
    Usage:
    \tfile <optional arguments> <sha256> OR <service>\n
    Parameters:
    \t<optional arguments>      The type of file operation being performed
    \t<sha256>                  The sha256 hash value of the file being operated on
    \t<service>                 The service that you're fetching the results for. type 'all' if you want results from
    \t                          all the services\n
    Optional Arguments:
    \t-d                        Download the file using the default encoding method. This api will force the browser in
    \t                          download mode
    \t-ga                       Return the ascii values for a file where ascii chars are replaced by DOTs
    \t-gc                       Get the list of children files for a given file
    \t-gh                       Returns the file hex representation
    \t-gi                       Get information about the file like: hashes, size, frequency count, etc
    \t-gr                       Get all the file results of a specific file
    \t-grs                      Get all the file results of a specific file and a specific query
    \t-gscor                    Get the score of the latest service run for a given file
    \t-gstr                     Return all strings in a given file
    \t-o, --out                 Output information to a file
    \t-m, --minimal             
    Example:
    \t# Download file
    \tfile -d 12345...67890\n
    \t# Get file ascii
    \tfile -ga 12345...67890\n
    \t# Get file children
    \tfile -gc 12345...67890\n
    \t# Get file hex
    \tfile -gh 12345...67890\n
    \t# Get file information
    \tfile -gi 12345...67890\n
    \t# Get file results
    \tfile -gr 12345...67890\n
    \t# Get file results for service
    \tfile -grs 12345...67890 all\n
    \t# Get file score
    \tfile -gscor 12345...67890\n
    \t# Get file strings
    \tfile -gstr 12345...67890
    """
    print(text)


# This function displays the help menu for the hash_search command
def help_hash_search():
    pass


# This function displays the help menu for the sysconfig command
def help_sysconfig():
    pass


# This function displays the help menu for the heuristics command
def help_heuristics():
    pass


# This function displays the help menu for the ingest command
def help_ingest():
    pass


# This function displays the help menu for the live command
def help_live():
    pass


# This function displays the help menu for the result command
def help_result():
    pass


# This function displays the help menu for the search command
def help_search():
    pass


# This function displays the help menu for the service command
def help_service():
    pass


# This function displays the help menu for the signature command
def help_signature():
    pass


# This function displays the help menu for the submissions command
def help_submission():
    text = """
    View and perform operations on submissions\n
    Usage:
    \tsubmission <optional arguments> <sid> OR <sha256> OR <group> OR <username> OR <verdict>
    Parameters:
    \t<optional arguments>     The type of submission operation being performed
    \t<sid>                    Submission ID required for some requests
    \t<sha256>                 Submission hash value required for some requests
    \t<group>                  Group name to get all related submissions
    \t<username>               Username to get all submissions for current user
    \t<verdict>                Verdict that the user gives a submission (malicious or non-malicious)\n
    Optional Arguments:
    \t-d, --delete             Delete a submission and it's related files, results, and errors
    \t-fsr                     Gets all results and errors of a specific file for a specific submission ID
    \t-ft                      Gets the file hierarchy of a given submission ID (limited to max depth set in system 
    \t                         settings
    \t-fr                      Gets the full results for a given submission ID. This will give you the actual values of
    \t                         the result and error keys instead of just listing the keys
    \t-r, --report             Creates a report for a submission based on its ID
    \t-sub, --submission       Gets the submission details for a given submission ID
    \t-sum, --summary          Retrieves the executive summary of a given submission ID. This is a MAP of tags to sha256
    \t                         combined with a list of generated Tags by summary type
    \t-c, --completed          Checks if the submission is complete
    \t-g, --group              Lists submissions for specific group
    \t-u, --user               Lists submissions for current user
    \t-v, --verdict            Sets the verdict of a submission bases on its ID
    \t-m, --malicious          For setting the verdict of a submission as malicious
    \t-s --safe                For setting the verdict of a submission as safe (non-malicious)\n
    Examples:
    \t# Delete submission
    \tsubmission -d 4E0iTOKxIk7c6Xr2VHpyi0\n
    \t# Get file submission results
    \tsubmission -fsr 4E0iTOKxIk7c6Xr2VHpyi0 69755....ca2192\n
    \t# Get file tree
    \tsubmission -ft 4E0iTOKxIk7c6Xr2VHpyi0\n
    \t# Get full results
    \tsubmission -fr 4E0iTOKxIk7c6Xr2VHpyi0\n
    \t# Get report
    \tsubmission -r 4E0iTOKxIk7c6Xr2VHpyi0\n
    \t# Get summary
    \tsubmission -sum 4E0iTOKxIk7c6Xr2VHpyi0\n
    \t# Check if submission is completed
    \tsubmission -c 4E0iTOKxIk7c6Xr2VHpyi0\n
    \t# List submissions for a specified group
    \tsubmission -g ALL\n
    \t# List submissions for current user
    \tsubmission -u john1234\n
    \t# Set verdict for a submission
    \tsubmission -v -m 4E0iTOKxIk7c6Xr2VHpyi0
    """
    print(text)


# This function displays the help menu for the submit command
def help_submit():
    text = """
    Submit files or URLs for submission\n
    Usage:
    \tsubmit <optional arguments> <source file> OR <URL> Or <sha256> OR <sid> OR <output>\n
    Parameters:
    \t<optional arguments>      What's being submitted to Assemblyline and which services are running
    \t<source file>             Absolute or relative path of file being submitted. The file MUST be surrounded by double
    \t                          ("") quotes
    \t<sha256>                  Hash value of the file being submitted. The hash MUST be surrounded by double ("")
    \t                          quotes
    \t<sid>                     Submission ID of the specified file for resubmission. The sid MUST be surrounded by
    \t                          double ("") quotes
    \t<URL>                     URL to be submitted. The URL MUST be surrounded by double ("") quotes
    \t<output>                  The output file where the returned data will be saved\n
    Optional Arguments:
    \t-f, --file                Path to file or directory
    \t-h, --hash                sha256 hash value of the file
    \t-u, --url                 Link of the URL being submitted
    \t-ra                       Resubmit a submission for analysis with the exact same parameters as before
    \t-rda                      Resubmit a file for dynamic analysis
    \t-o, --out                 Output results to the file specified\n
    Examples:
    \t# Submitting a file for scanning
    \tsubmit -f "~/Documents/foo.txt"\n
    \t# Output results to a file
    \tsubmit -f "~/Documents/foo.txt" -o ~/Documents/results.txt\n
    \t# Submitting a URL for scanning
    \tsubmit -u "https://www.google.com"\n
    \t# Submitting a file for scanning (by hash value)
    \tsubmit -h "12345...67890"\n
    \t# Resubmit submissions for analysis
    \tsubmit -ra "12fad...faf97"\n
    \t# Resubmit for dynamic analysis
    \tsubmit -rda "12345...67890"
    """
    print(text)


# This function displays the help menu for the user command
def help_user():
    pass


# This function displays the help menu for the webauthn command
def help_webauthn():
    pass


# This function displays the help menu for the workflow command
def help_workflow():
    pass


# Dictionary of help commands and their corresponding functions
help_commands_list = {"alert": help_alert,
                      "auth": help_auth,
                      "bundle": help_bundle,
                      "documentation": help_documentation,
                      "error": help_error,
                      "file": help_file,
                      "hash_search": help_hash_search,
                      "heuristics": help_heuristics,
                      "ingest": help_ingest,
                      "live": help_live,
                      "result": help_result,
                      "search": help_search,
                      "service": help_service,
                      "signature": help_signature,
                      "submission": help_submission,
                      "submit": help_submit,
                      "sysconfig": help_sysconfig,
                      "user": help_user,
                      "webauthn": help_webauthn,
                      "workflow": help_workflow}
