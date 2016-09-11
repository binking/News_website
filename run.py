import os
from test_website.app import create_app
from test_website.settings import ProdConfig, OSxConfig


if os.environ.get("NEWS_WEBSITE_ENV") == 'osx':
    news_web = create_app(OSxConfig)
else:
    news_web = create_app(ProdConfig)

if __name__=="__main__":
    news_web.run(host='0.0.0.0', port=5000, debug=True)
