import React from 'react';
import ReactDOM from 'react-dom/client';

import './index.css';
import App from './App';

import DocumentMeta from 'react-document-meta';
import Readme from './Readme';


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
    <DocumentMeta {...meta} />
    <Readme />
    <hr className="mainhr" />
    <App />
  </React.StrictMode>
);
