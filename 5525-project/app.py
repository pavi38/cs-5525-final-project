from flask import Flask, jsonify, request
import boto3
import os

app = Flask(__name__)

# Configure AWS credentials and region
AWS_REGION = "us-east-2"
AWS_ACCOUNT_ID = "your-aws-account-id"
DASHBOARD_ID = "your-dashboard-id"
USER_ARN = "arn:aws:quicksight:us-east-2:your-aws-account-id:user/default/your-username"

boto3.setup_default_session(region_name=AWS_REGION)
quicksight = boto3.client('quicksight')


@app.route('/api/get-quicksight-url', methods=['GET'])
def get_quicksight_url():
    try:
        # Generate embed URL
        response = quicksight.get_dashboard_embed_url(
            AwsAccountId=AWS_ACCOUNT_ID,
            DashboardId=DASHBOARD_ID,
            IdentityType='IAM',
            UserArn=USER_ARN,
            SessionLifetimeInMinutes=60,
            UndoRedoDisabled=False,
            ResetDisabled=False
        )

        embed_url = response.get("EmbedUrl")
        if not embed_url:
            return jsonify({"error": "Failed to generate embed URL"}), 500

        return jsonify({"embedUrl": embed_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
