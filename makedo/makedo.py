import argparse
import logging
import re
import secrets
import socket
import subprocess
import sys

from flask import Flask, render_template_string, request, g, redirect, url_for
import yaml

app = Flask(__name__)
token = secrets.token_hex(16)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

args = None
results = None
config = None

def remove_escape_sequences(text):
    return re.sub(r'\x1b[^a-zA-Z]*[a-zA-Z]', '', text)

def parse_output(output, patterns):
    result = []
    output = remove_escape_sequences(output.decode('utf-8'))
    lines = output.split("\n")
    multiline_buffer = ""
    for i, line in enumerate(lines):
        for pattern in patterns:
            if re.search(pattern["regex"], line, re.IGNORECASE):
                multiline_buffer = line
                next_line_index = i + 1
                while next_line_index < len(lines) and not any(
                    re.search(p["regex"], lines[next_line_index], re.IGNORECASE)
                    for p in patterns
                ):
                    multiline_buffer += "\n" + lines[next_line_index]
                    next_line_index += 1
                result.append({"type": pattern["name"], "message": multiline_buffer})
                break
    return result

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stderr = b''
    for line in process.stdout:
        sys.stderr.buffer.write(line)
        stderr += line
    process.wait()
    if process.returncode == 0:
        return b''
    return stderr

@app.route(f"/{token}/", methods=["GET", "POST"])
def index():
    global results

    if request.method == "POST":
        output = execute_command(args.command)
        results = parse_output(output, config["patterns"])
        return redirect(url_for('index'))

    return render_template_string(template, results=results)

template = '''
<!DOCTYPE html>
<html>
<head>
    <title>makedo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <style>
        body {
            padding: 20px;
        }
        .message {
            font-family: monospace;
            white-space: pre;
        }
        .table-wrapper {
            overflow: auto;
        }
    </style>
</head>
<body>
    <h1>makedo</h1>
    <form id="reexecute-form" method="post" class="mb-3">
        <input type="submit" value="Re-execute Command" class="btn btn-primary">
    </form>
    {% if results %}
    <div class="table-wrapper">
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>Type</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
                {% for result in results %}
                <tr>
                    <td>{{ result.type }}</td>
                    <td class="message">{{ result.message }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}
    <script>
        document.addEventListener("keydown", function(event) {
            if (event.key === "F4") {
                event.preventDefault();
                document.getElementById("reexecute-form").submit();
            }
        });
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
</body>
</html>
'''

def main():
    global args
    global config
    global results

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=14341, help="Port to listen on")
    parser.add_argument("command", help="Command to execute and parse the output")
    args = parser.parse_args()

    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    output = execute_command(args.command)

    results = parse_output(output, config["patterns"])

    if not results:
        exit(0)

    print(f"http://{socket.gethostname()}:{args.port}/{token}/")
    app.run(host=socket.gethostname(), port=args.port)


if __name__ == "__main__":
    main()
