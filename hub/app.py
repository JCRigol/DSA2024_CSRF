from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import subprocess
# import logging
import bleach
import redis
import os

app = Flask(__name__)
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
CORS(app, origins=['http://localhost:5002'])

redis_client = redis.StrictRedis.from_url(os.getenv('REDIS_URL'))

admin_agent = {
    'admin_action_1':
    {
        'desc': 'The Admin of X.com wants to work on his pages finances, so he opens it on his browser',
        'status': 'Untouched'
    },
    'admin_action_2':
    {
        'desc': 'The Admin now logs into the page with his admin credentials',
        'status': 'Untouched'
    },
    'admin_action_3':
    {
        'desc': 'The Admin finishes his work, so he goes to Y.com to relax',
        'status': 'Untouched'
    },
    'admin_action_4':
    {
        'desc': 'The Admin sees a button named submit, and clicks it without thinking',
        'status': 'Untouched'
    }
}

@app.route('/')
def dashboard():
    return render_template('app.html', admin_agent=admin_agent)

@app.route('/update_admin', methods=['POST'])
def update_admin():
    global admin_agent

    admin_action_id = request.json.get('admin_action_id')
    status = request.json.get('status')
    admin_agent[admin_action_id] = status

    return jsonify(success=True)

@app.route('/reset_admin', methods=['POST'])
def reset_admin():
    for action in admin_agent:
        admin_agent[action]['status'] = 'Untouched'
    
    # app.logger.info(admin_agent)
    
    return redirect(url_for('dashboard'))

@app.route('/update_site', methods=['POST'])
def update_site():
    input_html = request.json.get('input_html')
    redis_client.publish('data-channel', input_html)
    sanitized_html, cleaned = sanitize_html(input_html)

    if cleaned:
        sanitized_html = 'The HTML sent had disallowed elements, so it was cleaned. This is what remains.\n' + sanitized_html

    return jsonify(sanitized_html=sanitized_html)

#Automatic admin call to run
@app.route('/run_admin', methods=['POST'])
def run_admin():
    result = subprocess.Popen(
        ['python3', 'sillyadmin.py'],
        stdout=subprocess.PIPE,
        text=True
    )
    
    for line in result.stdout:
        # app.logger.info(f'STDOUT: {line.strip()}')
        action_n = 1
        if line.strip() != 'error':
            action = 'admin_action_' + str(line.strip())
            admin_agent[action]['status'] = 'Cleared'
            action_n += 1
        else:
            action = 'admin_action_' + str(action_n)
            admin_agent[action]['status'] = 'Failed'

    return jsonify({
        'stdout': 'hi'
    })
    
#Mirror of the sanitization of the HTML in site2
def sanitize_html(vulnerable_html):
    #Minimum tags needed
    allowed_tags = [
        'form',
        'input',
        'button'
    ]

    #Minimum attributes needed per tag
    allowed_attributes = {
        '*': ['action', 'method'],
        'input': ['type', 'name', 'value'],
        'button': ['type', 'name']
    }

    sanitized_html = bleach.clean(
        vulnerable_html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )

    return sanitized_html, (sanitized_html != vulnerable_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

