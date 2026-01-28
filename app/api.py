from flask import Flask, request, jsonify, abort
from src.account_registry import AccountsRegistry
from src.account import Account

app = Flask(__name__)
registry = AccountsRegistry()


def _parse_amount(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _get_json():
    return request.get_json(silent=True) or {}

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = _get_json()
    if not {"name", "surname", "pesel"}.issubset(data):
        return jsonify({"message": "Invalid account data"}), 400
    if registry.find_by_pesel(data["pesel"]):
        return jsonify({"message": "Account with this pesel already exists"}), 409
    account = Account(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.all_accounts()
    accounts_data = [
        {
            "name": acc.first_name,
            "surname": acc.last_name,
            "pesel": acc.pesel,
            "balance": acc.balance,
        }
        for acc in accounts
    ]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    return jsonify({"count": registry.count()}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    acc = registry.find_by_pesel(pesel)
    if not acc:
        abort(404)
    return jsonify(
        {"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance}
    ), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    acc = registry.find_by_pesel(pesel)
    if not acc:
        abort(404)
    data = _get_json()
    if "name" in data:
        acc.first_name = data["name"]
    if "surname" in data:
        acc.last_name = data["surname"]
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    if not registry.remove_by_pesel(pesel):
        abort(404)
    return jsonify({"message": "Account deleted"}), 200


@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    acc = registry.find_by_pesel(pesel)
    if not acc:
        abort(404)

    data = _get_json()
    if "amount" not in data or "type" not in data:
        return jsonify({"message": "Invalid transfer data"}), 400

    amount = data["amount"]
    kind = data["type"]

    transfers = {
        "incoming": acc.receive_transfer,
        "outgoing": acc.send_transfer,
        "express": acc.send_express_transfer,
    }
    if kind not in transfers:
        return jsonify({"message": "Unknown transfer type"}), 400

    ok = transfers[kind](amount)
    if ok:
        return jsonify(
            {"message": "Zlecenie przyjęto do realizacji", "balance": acc.balance}
        ), 200

    if kind in {"outgoing", "express"} and ok is False:
        return jsonify({"message": "Transfer rejected"}), 422
    if kind == "incoming" and ok is False:
        return jsonify({"message": "Invalid amount"}), 400

    return jsonify({"message": "Zlecenie przyjęto do realizacji", "balance": acc.balance}), 200