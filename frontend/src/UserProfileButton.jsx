import React from "react";
import { Link } from 'react-router-dom';
import { useAuth0 } from "@auth0/auth0-react";

import './Header.css'

const UserProfileButton = () => {
  const { user, isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return <></>
  }

  return (
      isAuthenticated ? (
        <Link className='navlink' to="/userprofile">Korisnički profil</Link>
      ) : (
        <span>
        {/* Not logged in */}
        </span>
      )
  );
};

export default UserProfileButton;