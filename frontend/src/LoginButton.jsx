import React from "react";
import { useAuth0 } from "@auth0/auth0-react";

import './Header.css';

const LoginButton = () => {
  const { isAuthenticated, isLoading, loginWithRedirect } = useAuth0();
  if (isLoading)
    return;
  
  return (
    !isAuthenticated ? (
      <button
          className="navlink"
          style={{ justifySelf: "flex-end" }}
          onClick={() => loginWithRedirect()}
      >
          Login
      </button>
    ) : (
      <> </>
    )
  );
};

export default LoginButton;