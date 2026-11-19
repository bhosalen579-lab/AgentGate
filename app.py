"""Simple web page for the Agent Gatekeeper. Run: python app.py  -> http://127.0.0.1:5000"""
from flask import Flask, request, redirect, render_template_string
import gatekeeper as g

app = Flask(__name__)
g.init()

PAGE = """
<!doctype html><title>Agent Gatekeeper</title>
<body style="font-family:Arial;max-width:900px;margin:20px auto">
<h1>Agent Gatekeeper - {{g.COMPANY}}</h1>
<h3>Enrolment No: {{g.ENROLMENT}}</h3>
{% if result %}<p style="padding:10px;background:#eef"><b>{{result[0]}}</b> | Rule {{result[1]}} | {{result[2]}}</p>{% endif %}

<h2>1. Register an agent</h2>
<form method="post" action="/register">Agent: <input name="agent"> Customer: <input name="customer"> <button>Register</button></form>

<h2>2. Send a request</h2>
<form method="post" action="/request">
Customer: <input name="customer"> Agent: <input name="agent">
Action: <select name="action">{% for a in g.ACTIONS %}<option>{{a}}</option>{% endfor %}</select>
Amount (Rs): <input name="amount" value="0" size="6"> <button>Decide</button></form>

<h2>Agents</h2>
<table border=1 cellpadding=4><tr><th>Agent</th><th>Customer</th><th>Registered</th><th>Revoked at</th><th></th></tr>
{% for a in agents %}<tr><td>{{a.agent}}</td><td>{{a.customer}}</td><td>{{a.registered_at}}</td><td>{{a.revoked_at or '-'}}</td>
<td>{% if not a.revoked_at %}<form method="post" action="/revoke"><input type="hidden" name="agent" value="{{a.agent}}"><button>Revoke</button></form>{% endif %}</td></tr>{% endfor %}</table>

<h2>Audit log</h2>
<table border=1 cellpadding=4><tr><th>Time</th><th>Customer</th><th>Agent</th><th>Action</th><th>Amount</th><th>Decision</th><th>Rule</th></tr>
{% for r in log %}<tr><td>{{r.ts}}</td><td>{{r.customer}}</td><td>{{r.agent}}</td><td>{{r.action}}</td><td>{{r.amount}}</td><td>{{r.decision}}</td><td>{{r.rule}}</td></tr>{% endfor %}</table>
</body>"""


def show(result=None):
    with g.db() as c:
        agents = c.execute("SELECT * FROM agents").fetchall()
        log = c.execute("SELECT * FROM audit ORDER BY id DESC LIMIT 30").fetchall()
    return render_template_string(PAGE, g=g, agents=agents, log=log, result=result)


@app.route("/")
def home():
    return show()


@app.route("/register", methods=["POST"])
def reg():
    g.register(request.form["agent"], request.form["customer"])
    return redirect("/")


@app.route("/revoke", methods=["POST"])
def rev():
    g.revoke(request.form["agent"])
    return redirect("/")


@app.route("/request", methods=["POST"])
def req():
    f = request.form
    return show(g.decide(f["customer"], f["agent"], f["action"], float(f["amount"] or 0)))


if __name__ == "__main__":
    app.run(debug=True)
