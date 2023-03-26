# makedo

makedo is a command output parser that filters error, warning, and note
messages from the output of a given command. It uses Flask to display the
parsed results in a web interface.  The command can be re-executed from
the web interface.

## Installation

To install makedo, you can use pip:

```bash
pip install makedo
```

## Usage

  1. Create a ~/.config/makedo.yaml file with the patterns you want to match in the command output. For example:
     ```yaml
     patterns:
       - name: Error
         regex: "error:"
       - name: Warning
         regex: "warning:"
       - name: Note
         regex: "note:"
     ```
  2. Run makedo with the command you want to execute and parse:
     ```bash
     makedo "your-command-here"
     ```
  3. Open your web browser and navigate to http://localhost:14341/ to view the parsed results.
  4. Press the "Re-execute Command" button or press the F4 key to re-run the command and update the parsed results.
