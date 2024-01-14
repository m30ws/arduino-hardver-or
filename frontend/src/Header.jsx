import { Link } from 'react-router-dom';
import './Header.css';

import './LoginButton'
import LoginButton from './LoginButton';
import LogoutButton from './LogoutButton';
import UserProfileButton from './UserProfileButton';
import SnapshotDatabaseButton from './SnapshotDatabaseButton';

import { useAuth0 } from "@auth0/auth0-react";

function Header() {
  return (
    <nav className="navBar">

      {/* Home */}
      <Link className='navlink' to="/">Home</Link>

      {/* Datatable */}
      <Link className='navlink' to="/datatable">Datatable</Link>

      {/* Login */}
      <LoginButton />

      {/* Logout */}
      <LogoutButton />

      {/* User profile */}
      <UserProfileButton />

      {/* Refresh files */}
      <SnapshotDatabaseButton />
      
    </nav>
  );
}

export default Header;