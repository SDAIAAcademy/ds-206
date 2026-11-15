# %% [markdown]
# # Setup check
#
# Run this notebook once before Day 1. It builds the synthetic tables of Hudhud Parcel, checks them
# against the reference numbers of the course, and tells you whether a hosted model is reachable.
#
# No key is needed for the course: every lab also runs on recorded replies. The recorded replies are
# scripted for the course, to carry the choices and errors it teaches; they are not captured from a product.
#
# All data is synthetic and describes nobody.

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-206.git"
    if not Path("/content/ds-206").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-206"], check=True)
    os.chdir("/content/ds-206/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import pandas as pd
import hudhud as U

pd.set_option("display.width", 160)
con = U.con()  # the first call builds the synthetic tables, once (about 20 seconds)

# %% [markdown]
# ## 1 · The tables

# %%
rows = {t: int(U.one(con, f"SELECT COUNT(*) FROM {t}")) for t in U.TABLES}
for t, n in rows.items():
    print(f"{t:14s} {n:>9,} rows")
U.check(rows == U.reference("rows"), "every table has the row count of the reference")

# %% [markdown]
# ## 2 · One number, computed here
#
# The share of dispatched parcels delivered at or before the promised cut-off, real customers only.
# You will meet this number, and five others that answer the same request, on Day 1.

# %%
rate = U.one(con, """
    SELECT AVG(CASE WHEN d.delivered_at <= d.promised_by THEN 1.0 ELSE 0.0 END)
    FROM deliveries d JOIN customers c USING (customer_id)
    WHERE c.segment <> 'TEST' AND d.status <> 'cancelled'""")
print(f"on-time rate: {rate:.4f}")
U.check(abs(rate - U.reference("on_time")) < 1e-4, "the rate matches the reference to four decimals")

# %% [markdown]
# ## 3 · A recorded reply runs
#
# The assistant of the course replies with code, and the notebook runs it here. Only table and column
# names are ever sent to a model.

# %%
reply = U.recorded("1.1", "one_line")
U.show(reply)
out = U.run_reply(reply, con)
U.check(out.error == "" and out.result is not None, "the recorded reply ran in this notebook")

# %% [markdown]
# ## 4 · A hosted model, if you have a key
#
# Optional. Set `OPENROUTER_API_KEY` in the environment (in Colab: the key icon, then
# `os.environ["OPENROUTER_API_KEY"] = userdata.get("OPENROUTER_API_KEY")`). The labs use a free hosted
# model; `HUDHUD_MODEL` chooses another, and `HUDHUD_BASE_URL` points the helper at any service that
# speaks the same chat protocol, including a model served on your own machine.

# %%
if U.has_key():
    live = U.ask("Reply with one line of Python that sets result to the number of rows in hubs.", tables=["hubs"], c=con, temperature=0)
    print("hosted model:", "answered" if live else "did not answer; the labs will use recorded replies")
else:
    print("No key set. The labs will use recorded replies, which is fine.")
print("\nSetup complete.")
