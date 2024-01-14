import './UserProfile.css';

import React, { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";

const UserProfile = () => {
  const { user, isLoading, isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [userMetadata, setUserMetadata] = useState(null);

  useEffect(() => {
    if (!user)
      return

    const getUserMetadata = async () => {
      try {
        const accessToken = await getAccessTokenSilently({
          authorizationParams: {
            // audience: `${process.env.REACT_APP_AUTH0_AUDIENCE}`,
            audience: `https://${process.env.REACT_APP_AUTH0_DOMAIN}/api/v2/`,
            scope: "read:active_user",
          },
        });
  
        const userDetailsByIdUrl = `https://${process.env.REACT_APP_AUTH0_DOMAIN}/api/v2/users/${user.sub}`;
        const metadataResponse = await fetch(userDetailsByIdUrl, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
  
        const { user_metadata } = await metadataResponse.json();  
        setUserMetadata(user_metadata);

      } catch (e) {
        console.log(e.message);
      }
    };
  
    getUserMetadata();
  }, [user, getAccessTokenSilently, user?.sub]);

  if (isLoading)
    return;

  return (
    isAuthenticated ? (
      <div className="userprofile">

        <img src={user.picture} alt={user.name} />
        
        <div style={{fontSize: "4em", fontWeight: 600, marginTop: "20px"}}>{user.name}</div>
        <div style={{fontSize: "2em", fontWeight: 400, marginTop: "5px", marginBottom: "20px"}}><span style={{fontWeight: 600}}>Nick: </span>{user.nickname}</div>
        
        <p style={{marginTop: "25px", fontSize: "2em"}}>
          <span style={{fontWeight: 600}}>Email: </span>
          <span >{user.email} </span>
          <span style={{fontSize: "0.65em"}}>{user.email_verified ? ("") : ("(unverified)")}</span>
        </p>
        
        {/* <div style={{fontSize: "2em", fontWeight: 400, marginTop: "5px", marginBottom: "20px"}}><span style={{fontWeight: 600}}>Web: </span>{user.website ? user.website : (<em>no website.</em>)}</div>

        <div style={{fontSize: "2em", fontWeight: 400, marginTop: "5px", marginBottom: "20px"}}><span style={{fontWeight: 600}}>Birthday: </span>{user.birthdate ? user.birthdate : (<em>no birthday.</em>)}</div> */}

        <span style={{fontSize: "1.2em"}}><em>Auth0 ID: {user.sub}</em></span>

        {userMetadata ? (
          <div>
            <h3>Additional metadata: </h3>
            <pre>{JSON.stringify(userMetadata, null, 2)}</pre>
          </div>
        ) : (
          <div>
            {/* No other metadata found. */}
          </div>
        )}
        
      </div>
    ) : (
      <div>
        {/* <NotFound /> */}
        <div>
          <div className="titl">
            Unauthorized !
          </div>
          <div className="msgg">
            Use login button to gain access to profile info.
          </div>
        </div>
      </div>
    )
  );
};

export default UserProfile;