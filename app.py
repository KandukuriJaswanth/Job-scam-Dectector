from flask import Flask, request, jsonify, send_file
import re
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('templates/sai.html')


# Regex Matcher Tool - Find Matches
@app.route('/regex_results', methods=['POST'])
def regex_results():
    test_string = request.form['test_string']
    regex_pattern = request.form['regex_pattern']

    try:
        matches = re.findall(regex_pattern, test_string)
    except re.error:
        matches = ['Invalid Regex Pattern']

    return jsonify({
        'test_string': test_string,
        'regex_pattern': regex_pattern,
        'matches': matches
    })


# Regex Matcher Tool - Email Validation
@app.route('/validate_email', methods=['POST'])
def validate_email():
    email = request.form['email']
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = re.match(email_regex, email) is not None

    return jsonify({'email': email, 'valid': is_valid})


# Fake Job Detector - Detect suspicious job post
@app.route('/fake_job_results', methods=['POST'])
def fake_job_results():
    company_name = request.form['company_name']
    address = request.form['address']

    suspicious_keywords = ['lottery', 'winner', 'urgent', 'free', 'money', 'investment']
    suspicious_count = sum(1 for keyword in suspicious_keywords if keyword.lower() in address.lower())

    is_suspicious = suspicious_count > 0
    verdict = 'Suspicious - Contains suspicious keywords' if is_suspicious else 'Looks okay'

    # Optional: Add Google, LinkedIn, Naukri search links in the response
    google_link = f"https://www.google.com/search?q={company_name.replace(' ', '+')}"
    linkedin_link = f"https://www.linkedin.com/search/results/all/?keywords={company_name.replace(' ', '+')}"
    naukri_link = f"https://www.naukri.com/{company_name.replace(' ', '-')}-jobs"

    return jsonify({
        'company_name': company_name,
        'address': address,
        'verdict': verdict,
        'suspicious_count': suspicious_count,
        'search_links': {
            'google': google_link,
            'linkedin': linkedin_link,
            'naukri': naukri_link
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
