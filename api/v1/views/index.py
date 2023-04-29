#!/usr/bin/python3
"""
Flask app
"""
from api.v1.views import app_views
from flask import Flask, render_template, jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """status"""
    return (jsonify({"status": "OK"}))
