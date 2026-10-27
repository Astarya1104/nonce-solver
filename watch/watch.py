import json, os, time, urllib.request, subprocess
URL = "https://mcp.nonceprotocol.xyz/mcp"
BODY = json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"protocol_info","arguments":{}}}).encode()
END = time.time() + float(os.environ.get("RUN_SECONDS", "20700"))
INTERVAL = int(os.environ.get("INTERVAL", "120"))

def info():
    req = urllib.request.Request(URL, data=BODY, headers={"content-type":"application/json","accept":"application/json, text/event-stream","user-agent":"nonce-watch"})
    o = urllib.request.urlopen(req, timeout=45).read().decode()
    if "data:" in o[:30]:
        o = "\n".join(l[5:].strip() for l in o.splitlines() if l.startswith("data:"))
    t = json.loads(o)["result"]["content"][0]["text"]
    d = json.loads(t)
    return d[0] if isinstance(d, list) else d

STATUS = "https://nonceprotocol.xyz/api/status"
def status():
    req = urllib.request.Request(STATUS, headers={"user-agent":"nonce-watch","accept":"application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode())

def gh(*a):
    return subprocess.run(["gh", *a], capture_output=True, text=True)

def already_open():
    r = gh("issue", "list", "--label", "admission-open", "--state", "open", "--json", "number")
    try: return len(json.loads(r.stdout or "[]")) > 0
    except Exception: return False

while time.time() < END:
    try:
        st = status()
        mode = st.get("mode", ""); paused = (st.get("onchain") or {}).get("paused"); sup = (st.get("onchain") or {}).get("totalSupply")
        is_open = ("closed" not in mode.lower()) or paused is False
        d = {}; b = {}; v = c = ratio = None; adm = "open" if is_open else "closed"
        if is_open:
            for i in range(4):
                try: d = info(); break
                except Exception as e: print("mcp retry", i, e); time.sleep(5 + 5*i)
            if d.get("admission") == "closed" and paused is not False: adm = "closed"
            b = d.get("benchmark") or {}
            v, c = b.get("variables"), b.get("clauses")
            ratio = round(c / v, 2) if v and c else None
        print(time.strftime("%H:%M:%S"), mode, "paused=", paused, "supply=", sup, d.get("version"), ratio, flush=True)
        if adm == "open" and not already_open():
            title = f"NONCE admission OPEN - {d.get('version')} ratio {ratio}"
            body = (f"admission: open\nstatus mode: {mode}\nonchain paused: {paused}\ntotalSupply: {sup}\nversion: {d.get('version')}\nvariables: {v}\nclauses: {c}\n"
                    f"literalsPerClause: {b.get('literalsPerClause')}\nratio: {ratio}\n"
                    f"deadlineSeconds: {b.get('deadlineSeconds')}\n\n"
                    "Ratio <=19: solvable in seconds. Ratio >=20: practically unsolvable.\n"
                    "Open Hark and reply to start an attempt.")
            gh("label", "create", "admission-open", "--color", "d73a4a", "--force")
            r = gh("issue", "create", "--title", title, "--body", body, "--label", "admission-open", "--assignee", os.environ.get("OWNER", "voozie100"))
            print("issue", r.returncode, r.stdout, r.stderr, flush=True)
        elif adm != "open" and already_open():
            r = gh("issue", "list", "--label", "admission-open", "--state", "open", "--json", "number")
            for it in json.loads(r.stdout or "[]"):
                gh("issue", "close", str(it["number"]), "--comment", "admission closed again " + time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()))
    except Exception as e:
        print("err", e, flush=True)
    time.sleep(INTERVAL)
