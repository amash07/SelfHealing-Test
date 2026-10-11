import os
import sys
import time
import subprocess
import re
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "self-healing-demo-secret"

# Demo credentials
USERNAME = "admin"
PASSWORD = "admin123"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))

        error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session.get("username", "Student")
    )


@app.route("/profile")
def profile():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        username=session.get("username", "Student")
    )


@app.route("/settings")
def settings():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("settings.html")


@app.route("/products")
def products():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("products.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ========================================================
# TEST RUNNER & LIVE DEMO ROUTES
# ========================================================

@app.route("/demo")
@app.route("/runner")
@app.route("/test-runner")
def demo_runner():
    return render_template("demo.html")


@app.route("/api/run-test", methods=["POST"])
def run_test_api():
    data = request.get_json() or {}
    mode = data.get("mode", "without_healing")
    is_headless = data.get("headless", False)

    if mode == "without_healing":
        script_path = os.path.join(PROJECT_ROOT, "tests", "test_without_healing.py")
    else:
        script_path = os.path.join(PROJECT_ROOT, "tests", "test_student_portal.py")

    cmd = [sys.executable, script_path]
    if is_headless:
        cmd.append("--headless")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    start_time = time.time()
    try:
        process = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=45
        )
        duration = time.time() - start_time
        raw_output = process.stdout + ("\n" + process.stderr if process.stderr else "")
        exit_code = process.returncode
    except subprocess.TimeoutExpired:
        duration = 45.0
        raw_output = "Error: Test run timed out after 45 seconds."
        exit_code = 1
    except Exception as e:
        duration = time.time() - start_time
        raw_output = f"Execution error: {str(e)}"
        exit_code = 1

    # Parse output telemetry
    parsed = parse_test_telemetry(raw_output, mode, exit_code)

    return jsonify({
        "status": parsed["overall_status"],
        "duration": duration,
        "exit_code": exit_code,
        "mode": mode,
        "raw_output": raw_output.strip(),
        "healed_count": parsed["healed_count"],
        "steps": parsed["steps"]
    })


def parse_test_telemetry(output: str, mode: str, exit_code: int):
    steps = []
    healed_count = 0
    overall_status = "PASSED" if ("ALL TESTS PASSED" in output and exit_code == 0) else "FAILED"

    # Define known steps in flow
    step_names = [
        "TEST 1: Login",
        "TEST 2: Dashboard",
        "TEST 3: Profile",
        "TEST 4: Products",
        "TEST 5: Settings",
        "TEST 6: Logout"
    ]

    for name in step_names:
        if name in output:
            # Extract section for this test
            start_idx = output.find(name)
            # Find next test index or end
            next_indices = [output.find(nxt, start_idx + len(name)) for nxt in step_names if output.find(nxt, start_idx + len(name)) != -1]
            end_idx = min(next_indices) if next_indices else len(output)
            step_chunk = output[start_idx:end_idx]

            is_healed = "SELF-HEALING ACTIVATED" in step_chunk
            if is_healed:
                healed_count += 1

            orig_match = re.search(r"Original:\s*([^\r\n]+)", step_chunk)
            rec_match = re.search(r"Recovered:\s*([^\r\n]+)", step_chunk)
            score_match = re.search(r"Score:\s*(\d+)", step_chunk)

            if "PASS:" in step_chunk or (name == "TEST 2: Dashboard" and "PASS" in step_chunk):
                step_status = "passed"
                error_msg = None
            elif "TEST FAILED" in step_chunk or "Error:" in step_chunk or overall_status == "FAILED":
                step_status = "failed"
                err_match = re.search(r"Error:\s*([^\r\n]+)", step_chunk)
                error_msg = err_match.group(1) if err_match else "Locator lookup failed"
            else:
                step_status = "passed"
                error_msg = None

            steps.append({
                "name": name,
                "status": step_status,
                "healed": is_healed,
                "original_locator": orig_match.group(1).strip() if orig_match else None,
                "recovered_locator": rec_match.group(1).strip() if rec_match else None,
                "score": score_match.group(1) if score_match else None,
                "error": error_msg
            })

    if not steps and overall_status == "FAILED":
        steps.append({
            "name": "TEST 1: Login",
            "status": "failed",
            "healed": False,
            "error": "Failed before steps initialized. Check terminal output for stack trace."
        })

    return {
        "overall_status": overall_status,
        "healed_count": healed_count,
        "steps": steps
    }


if __name__ == "__main__":
    app.run(debug=True)