import sys, json, os, base64, urllib.request
T = os.environ["T"]
URL = "https://diana-rafael.myshopify.com/admin/api/2025-10/graphql.json"
def gql(q, v=None):
    r = urllib.request.Request(URL, json.dumps({"query": q, "variables": v or {}}).encode(), {"Content-Type": "application/json", "X-Shopify-Access-Token": T})
    return json.load(urllib.request.urlopen(r, timeout=120))
def get(tid, files):
    q = """query($id:ID!,$f:[String!]){theme(id:$id){name role files(filenames:$f,first:50){nodes{filename checksumMd5 size body{... on OnlineStoreThemeFileBodyText{content} ... on OnlineStoreThemeFileBodyBase64{contentBase64}}}}}}"""
    return gql(q, {"id": f"gid://shopify/OnlineStoreTheme/{tid}", "f": files})
def put(tid, filename, path, b64=False):
    data = open(path, "rb").read()
    body = {"type": "BASE64", "value": base64.b64encode(data).decode()} if b64 else {"type": "TEXT", "value": data.decode("utf-8")}
    q = """mutation($id:ID!,$files:[OnlineStoreThemeFilesUpsertFileInput!]!){themeFilesUpsert(themeId:$id,files:$files){upsertedThemeFiles{filename} userErrors{field message code}}}"""
    return gql(q, {"id": f"gid://shopify/OnlineStoreTheme/{tid}", "files": [{"filename": filename, "body": body}]})
if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "get":
        tid, out = sys.argv[2], sys.argv[3]
        r = get(tid, sys.argv[4:])
        t = r["data"]["theme"]; print(t["name"], t["role"])
        for n in t["files"]["nodes"]:
            b = n["body"]; fn = out + "/" + n["filename"].replace("/", "__")
            if "content" in b: open(fn, "w", encoding="utf-8", newline="").write(b["content"])
            else: open(fn, "wb").write(base64.b64decode(b["contentBase64"]))
            print(n["filename"], n["checksumMd5"], n["size"])
    elif cmd == "put":
        print(json.dumps(put(sys.argv[2], sys.argv[3], sys.argv[4], len(sys.argv) > 5 and sys.argv[5] == "b64")))
