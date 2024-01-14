import React from "react";
import { useState, useEffect } from 'react';

import { useAuth0 } from "@auth0/auth0-react";

import './Header.css';

const BACKEND = process.env.REACT_APP_BACKEND_URL;

const SnapshotDatabaseButton = () => {
  const { user, isAuthenticated, isLoading, getAccessTokenSilently, getAccessTokenWithPopup } = useAuth0();

  const fireSnapshot = async () => {

    let accessToken;
    try {
      accessToken = await getAccessTokenSilently({
        authorizationParams: {
          audience: `${process.env.REACT_APP_AUTH0_AUDIENCE}`,
          scope: "update:snapshot_database",
        },
      });

    } catch(e) {
      console.log(e.message);
      console.log("unable to get token silently; showing popup")

      try {
        accessToken = await getAccessTokenWithPopup({
          authorizationParams: {
            audience: `${process.env.REACT_APP_AUTH0_AUDIENCE}`,
            scope: "update:snapshot_database",
          },
        });
      } catch(ee) {
        console.log( )
      }
    }

    try {
      const snpResp = await fetch(`${BACKEND}/snapshot-database`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      const snpJsn = await snpResp.json();

      alert(snpJsn['message']);
    } catch(e) {
      console.log(e.message)
    }
  };

  if (isLoading) {
    return <></>
  }

  return (
      isAuthenticated ? (
        <button
            className="navlink"
            style={{ justifySelf: "flex-end" }}
            onClick={() => fireSnapshot()}
        >
            Osvježi preslike
        </button>

      ) : (
        <span>
        {/* Not logged in */}
        </span>
      )
  );
};

export default SnapshotDatabaseButton;