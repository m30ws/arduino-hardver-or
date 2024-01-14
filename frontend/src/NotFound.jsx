import './NotFound.css';

function NotFound() {
  return (
    <div>
      <div className="notfound-title">
        Sorry, invalid URL!
      </div>
      <div className="notfound-msg">
        Use navigation bar at the top to go back.
      </div>
    </div>
  );
}

export default NotFound;