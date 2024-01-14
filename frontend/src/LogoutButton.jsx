import React from "react";
import { useAuth0 } from "@auth0/auth0-react";

const LogoutButton = () => {
  const { isAuthenticated, isLoading, logout } = useAuth0();
  if (isLoading)
    return;
    
  return (
    isAuthenticated ? (
      <button
          className="navlink"
          style={{ justifySelf: "flex-end" }}
          onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
      >
        Logout
      </button>
    ) : (
      <> </>
    )
  );
};

export default LogoutButton;