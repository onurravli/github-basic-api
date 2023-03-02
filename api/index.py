from flask import Flask
from bs4 import BeautifulSoup as bs
import requests
import json

app = Flask(__name__)


@app.route('/')
def home():
    return 'github basic api.'


@app.route('/<string:user>')
def user_info(user):
    try:
        content = requests.get(f'https://github.com/{user}/')
        soup = bs(content.text, 'html.parser')
        user_name = soup.find(
            'span', {'class': 'p-name vcard-fullname d-block overflow-hidden'}).text.replace('\n', '')
        try:
            user_desc = soup.find(
                'div', {'class': 'p-note user-profile-bio mb-3 js-user-profile-bio f4'}).text.replace('\n', '')
        except AttributeError:
            user_desc = 'No description'
        user_image = soup.find(
            'img', {'class': 'avatar avatar-user width-full border color-bg-default'}).get('src').replace("?v=4", "")
        user_followers = soup.find_all(
            'span', {'class': 'text-bold color-fg-default'})[0].text.replace('\n', '')
        user_following = soup.find_all(
            'span', {'class': 'text-bold color-fg-default'})[1].text.replace('\n', '')
        return json.dumps({
            'user_name': user_name,
            'user_desc': user_desc,
            'user_image': user_image,
            'user_followers': user_followers,
            'user_following': user_following}, indent=4)
    except AttributeError:
        return json.dumps({'error': 'user not found'}, indent=4)


@app.route('/<string:user>/<string:repo>')
def repo_info(user, repo):
    try:
        content = requests.get(f'https://github.com/{user}/{repo}')
        soup = bs(content.text, 'html.parser')
        repo_name = soup.find(
            'strong', {'class': 'mr-2'}).text.replace('\n', '')
        try:
            repo_desc = soup.find(
                'p', {'class': 'f4 my-3'}).text.replace('\n', '')
        except AttributeError:
            repo_desc = 'No description'
        repo_star = soup.find(
            'span', {'id': 'repo-stars-counter-star'}).text.replace('\n', '')
        repo_fork = soup.find(
            'span', {'id': 'repo-network-counter'}).text.replace('\n', '')
        repo_last_commit = soup.find(
            'relative-time', {'class': 'no-wrap'}).text.replace('\n', '')
        return json.dumps({
            'repo_name': repo_name,
            'repo_desc': repo_desc,
            'repo_star': repo_star,
            'repo_fork': repo_fork,
            'repo_last_commit': repo_last_commit}, indent=4)
    except AttributeError:
        return json.dumps({'error': 'repo or user not found'}, indent=4)
