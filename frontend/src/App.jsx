import DocumentMeta from 'react-document-meta';
import { Routes, Route, Navigate } from 'react-router-dom';

import Header from './Header';
import Readme from './Readme';
import DatasetInterface from './DatasetInterface';
import UserProfile from './UserProfile';
import NotFound from './NotFound';
import './App.css';

function App({meta}) {
  return (
    <>
      <DocumentMeta {...meta} />
      <Header />
      <Routes>
        <Route index element={<Readme />} />
        <Route path="/readme" element={<Navigate replace to="/" />} />
        <Route path="/datatable" element={<DatasetInterface />} />
        <Route path="/userprofile" element={<UserProfile />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}

export default App;