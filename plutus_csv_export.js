javascript: (async function () {
    class Plutus {
        async #request(method, url, bodyParams = {}, returnType = null) {
            if (["get", "post", "put", "patch", "delete"].includes(method)) {
                const resp = await fetch(url, {
                    method: method,
                    headers: {
                        authorization: `Bearer ${localStorage.getItem("id_token")}`,
                        "content-type": "application/json"
                    },
                    body: Object.keys(bodyParams).length && method !== "get" ? JSON.stringify(bodyParams) : undefined
                });
                if (returnType === "json") {
                    return resp.json();
                }
                if (returnType === "text") {
                    return resp.text();
                }
                return resp;
            }
            console.warn(`Unsupported request method "${method}"`);
            return false;
        }
        #get(url, returnType) {
            return this.#request("get", url, {}, returnType);
        }
        #post(url, bodyParams, returnType) {
            return this.#request("post", url, bodyParams, returnType);
        }
        async getRewards() {
            return this.#get("https://api.plutus.it/platform/transactions/pluton", "json");
        }
        async getStatements() {
            const payload = {
                "operationName": "transactions_view",
                "variables": {
                    "offset": 0,
                    "limit": null
                },
                "query": "query transactions_view($offset: Int, $limit: Int, $from: timestamptz, $to: timestamptz, $type: String) {\n  transactions_view_aggregate(\n    where: {_and: [{date: {_gte: $from}}, {date: {_lte: $to}}]}\n  ) {\n    aggregate {\n      totalCount: count\n      __typename\n    }\n    __typename\n  }\n  transactions_view(\n    order_by: {date: desc}\n    limit: $limit\n    offset: $offset\n    where: {_and: [{date: {_gte: $from}}, {date: {_lte: $to}}, {type: {_eq: $type}}]}\n  ) {\n    id\n    model\n    user_id\n    currency\n    amount\n    date\n    type\n    is_debit\n    description\n    clean_description\n    confidence\n    name\n    url\n    plu_amount\n    original_transaction_id\n    mcc\n    reward_decline_reason\n    activity_id\n  }\n}\n"
            };
            return this.#post("https://hasura.plutus.it/v1alpha1/graphql", payload, "json");
        }
        async downloadRewardsCsv() {
            const rewards = await this.getRewards();
            const fields = Object.keys(rewards[0]).filter(v => v !== "fiat_transaction" && v !== "contis_transaction");
            const data = [fields, ...rewards.map(r => fields.map(f => r[f]))];
            downloadCsvRows("plutus-rewards.csv", data);
        }
        async downloadStatementsCsv() {
            const response = await this.getStatements();
            const statements = response.data.transactions_view;
            const fields = Object.keys(statements[0]);
            const data = [fields, ...statements.map(r => fields.map(f => r[f] ?? ''))];
            downloadCsvRows("plutus-statements.csv", data);
        }
    }

    function downloadFile(filename, text, mime) {
        const element = document.createElement("a");
        element.setAttribute("href", `data:${mime};charset=utf-8,${encodeURIComponent(text)}`);
        element.setAttribute("download", filename);
        element.click();
    }

    function downloadCsvRows(filename, data, separator = "|") {
        const csv = data.map(row => row.join(separator)).join("\n");
        downloadFile(filename, csv, "text/csv");
    }
    const plu = new Plutus;
    plu.downloadRewardsCsv();
})();
