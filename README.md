# dsp2019-tool

# Backend

## How to install

You have to have Python >=3.5 and pip installed.

1) I recommend using virtualenv to manage your installation, install it with pip if you haven't already. Then go to the `backend` folder and create environment called venv: `virtualenv venv`. (perhaps use `virtualenv -p python3 venv` if you have multiple Python installations eg macOS)
2) Activate it: `source ./venv/bin/activate`
3) Install the dependencies: `pip install -r requirements.txt`
4) Create a `backend/models` folder and Download or move your models there
5) Start the dev server: `./dev.sh` NOTE: if you want to use Github API specify a Github API key (can be a dummy, Github allows 500 request per day even without it): `GITHUB_API_KEY=asdf ./dev.sh`

## How to develop the API

Easy way to send requests to the backend is to use Visual Code with this extension called https://marketplace.visualstudio.com/items?itemName=humao.rest-client

Anyway after installing those simply open the `api-stuff.http` file and "Send Request" option should appear before any of the requests. Click that and it will send the request with parameters described in the text. Cool!

