# -*- coding: utf-8 -*-
from test_website.app import create_app
from test_website.settings import ProdConfig, OSxConfig


def test_production_config():
    app = create_app(ProdConfig)
    assert app.config['ENV'] == 'prod'
    assert app.config['DEBUG'] is False
    assert app.config['DEBUG_TB_ENABLED'] is False
    assert app.config['ASSETS_DEBUG'] is False


def test_dev_config():
    app = create_app(OSxConfig)
    assert app.config['ENV'] == 'dev'
    assert app.config['DEBUG'] is True
    assert app.config['ASSETS_DEBUG'] is True
