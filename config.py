import os

from dotenv import load_dotenv

load_dotenv()

context = os.getenv('context', 'bstack')
bstack_userName = os.getenv('bstack_userName', os.getenv('BSTACK_USERNAME'))
bstack_accessKey = os.getenv('bstack_accessKey', os.getenv('BSTACK_ACCESSKEY'))
platformName = os.getenv('platformName')
app_id = os.getenv('app_id', 'bs://sample.app')
platformName = os.getenv('platformName', 'android')
app_path = os.getenv('app_path', 'bs://sample.app')
timeout = float(os.getenv('timeout', '10.0'))

