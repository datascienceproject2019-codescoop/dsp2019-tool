#!/usr/bin/env bash

export REACT_APP_API_URL=https://teekoivi.users.cs.helsinki.fi/api

rm -r ../static || true && \
  npm run build && \
  mv ./build/** ../
