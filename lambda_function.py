import json
import boto3
import base64

bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name="us-east-2"
)


def lambda_handler(event, context):
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }

    # --- DEBUG / REQUEST INSPECTION ---
    # Supports both API Gateway REST API payload (v1) and HTTP API payload (v2)
    http_method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method")
    path = event.get("path") or event.get("rawPath") or event.get("requestContext", {}).get("http", {}).get("path")
    source_ip = (
        event.get("requestContext", {}).get("identity", {}).get("sourceIp")
        or event.get("requestContext", {}).get("http", {}).get("sourceIp")
    )

    print("=== REQUEST DEBUG START ===")
    print(f"Method: {http_method}")
    print(f"Path: {path}")
    print(f"Source IP: {source_ip}")
    print(f"Is Base64 Encoded: {event.get('isBase64Encoded', False)}")
    print(f"Headers Present: {list(event.get('headers', {}).keys())[:10]}")
    headers = event.get("headers", {}) or {}

    print(f"User-Agent: {headers.get('User-Agent') or headers.get('user-agent')}")
    print(f"Content-Type: {headers.get('Content-Type') or headers.get('content-type')}")
    print(f"Host: {headers.get('Host') or headers.get('host')}")
    print(f"CloudFront Viewer Country: {headers.get('CloudFront-Viewer-Country') or headers.get('cloudfront-viewer-country')}")
    print(f"Top-level Event Keys: {list(event.keys())}")
    print("=== REQUEST DEBUG END ===")

    # Handle preflight cleanly
    if http_method == "OPTIONS":
        print("Handled OPTIONS preflight request")
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": ""
        }

    # Only allow POST
    if http_method != "POST":
        print(f"Rejected non-POST request. Method received: {http_method}")
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json", **cors_headers},
            "body": json.dumps({"error": "Only POST is allowed for this endpoint."})
        }

    try:
        body_raw = event.get("body", "")
        is_base64 = event.get("isBase64Encoded", False)

        print(f"Raw body exists: {bool(body_raw)}")
        print(f"Raw body preview (first 200 chars): {str(body_raw)[:200]}")

        if is_base64 and body_raw:
            body_raw = base64.b64decode(body_raw).decode("utf-8")
            print("Body was base64 decoded successfully")

        body = json.loads(body_raw) if body_raw and body_raw.strip() else {}
        question = body.get("question", "").strip()

        print(f"Parsed question present: {bool(question)}")
        print(f"Question preview: {question[:100]}")

        if not question:
            print("Rejected request: missing or empty question")
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json", **cors_headers},
                "body": json.dumps({"error": "Ask something dumb first, bro... 😏"})
            }

        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "system": (
                "You are Hey Stupid. "
                "Reply with exactly one sentence, maximum 30 words. "
                "Be absurd, sarcastic, chaotic, and useless. "
                "Be dumber than necessary. "
                "Never explain or be useful; always be ridiculous. "
                "Misunderstand the question in the dumbest possible way. "
                "Throw in random unrelated nonsense and emojis."
            ),
            "max_tokens": 30,
            "temperature": 0.6,
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }

        print("Invoking Bedrock model...")

        response = bedrock_runtime.invoke_model(
            modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0",
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(response["body"].read())
        print(f"Bedrock response keys: {list(result.keys())}")

        answer = (
            result.get("content", [{}])[0].get("text", "").strip()
            or "Brain.exe has stopped working 🤡"
        )

        print(f"Answer preview: {answer[:150]}")
        print("Returning 200 success")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", **cors_headers},
            "body": json.dumps({"answer": answer})
        }

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json", **cors_headers},
            "body": json.dumps({"error": "That request was too stupid even for me. Invalid JSON."})
        }

    except Exception as e:
        print(f"Lambda exception: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", **cors_headers},
            "body": json.dumps({"error": "My stupidity crashed... try again?"})
        }