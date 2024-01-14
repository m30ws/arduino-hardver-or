import './Readme.css';
import './Header.css';

const BACKEND = process.env.REACT_APP_BACKEND_URL;

// function Readme({backend}) {
//   const BACKEND = backend;
function Readme() {
  return (
    <div style={{marginLeft: "20px", marginTop: "20px"}}>
      <div>
        <h2>Općenite informacije</h2>
        <b>Autor:</b> Fran Tomljenović
        <br/>
        <b>Verzija:</b> 4.0
        <br/>
        <b>Jezik:</b> Engleski
        <br/>   
      </div>
      <div>
        <br/>
        <a href={`${BACKEND}/boards/json`}>Download JSON file</a>
        <br/>
        <a href={`${BACKEND}/boards/csv`}>Download CSV file</a>
        <br/><br/>
      </div>
      <div
        style={{height: "100%", width:"100%"}}
      >
        This work is licensed under &nbsp;
        <a className="cclink"
          href={"http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1"}
          target={"_blank"}
          rel={"license noopener noreferrer"}
          style={{
            display: "inline-block",
            textDecoration: "none"
          }}
        >
          CC BY 4.0 &nbsp;
          <img style={{
              height: "30px",
              objectFit: "contain",
              marginLeft: "3px",
              verticalAlign: "text-bottom"
            }}
            src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"
            alt="" 
          />
          <img style={{
              height: "30px",
              objectFit: "contain",
              marginLeft: "3px",
              verticalAlign: "text-bottom"
            }}
            src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"
            alt=""
          />
        </a>
      </div>
    </div>
  );
}

export default Readme;