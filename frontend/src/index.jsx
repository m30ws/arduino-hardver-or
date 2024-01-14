import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { Auth0Provider } from '@auth0/auth0-react';

import './index.css';

import App from './App';

const meta = {
  title: 'Otvoreni podaci o Arduino razvojnim pločicama',
  description: 'Repozitorij sadrži otvoreni skup podataka o dijelu Arduino razvojnih pločica te nekim njihovim tehničkim karakteristikama i mogućnostima.',
  author: 'Fran Tomljenović',
  meta: {
      charset: 'utf-8',
      name: { keywords: 'arduino,react,fer' }
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Auth0Provider
      domain={process.env.REACT_APP_AUTH0_DOMAIN}
      clientId={process.env.REACT_APP_AUTH0_CLIENTID}
      authorizationParams={{
        redirect_uri: window.location.origin,
        audience: process.env.REACT_APP_AUTH0_AUDIENCE,
      }}
    >
      <BrowserRouter basename="/">
        <App meta={meta}/>
      </BrowserRouter>
    </Auth0Provider>
  </React.StrictMode>
);
