import './App.css';

import DataTable from 'react-data-table-component';
import { useState, useEffect } from 'react';

import Filter from './Filter'

const backend = 'http://localhost:5002';

function App() {
  const [schema, setSchema] = useState();

  const [columns, setColumns] = useState([]);
  const [data, setData] = useState([]);

  // <button onClick={}></button>

  const fetchdata = () => {
    // Acquire schema
    fetch(`${backend}/get-schema`)
    .then((resp) => {
      resp.json().then((jsn) => {
        setSchema(jsn);

        const schemaprops = jsn["items"]["properties"]
        const cols = Object.keys(schemaprops);

        let prepped = [];
        for (const prop of cols) {
          prepped.push({
            name: schemaprops[prop]["title"],
            selector: row => {
              if (prop === "microcontroller") {
                return row[prop]["microcontroller_name"];
              } else if (prop === "pins") {
                return row[prop]["pin_type"];
              } else {
                return row[prop];
              }
            },
            sortable: true,
          });
        }

        setColumns(prepped);
        console.log("prepped")
        console.log(prepped);
      })
    })

    // Acquire json data
    fetch(`${backend}/get-full-json`)
    .then((resp) => {
      resp.json().then((jsn) => {
        console.log("json data.")
        console.log(jsn.data);
        setData(jsn.data);
      })
    })
  }

  // On load
  useEffect(() => {
    fetchdata()
  },[])

  const ExpandedComponent = ({ data }) => {
    if (!data)
    return

///////////////////////////////////
////    MICROCONTROLLER
///////////////////////////////////
    const microschema = schema["items"]["properties"]["microcontroller"]['properties'];

    let mycolmicro = [];
    let keys = Object.keys(microschema)

    const schemaprops = schema["items"]["properties"]["microcontroller"]

    for (const prop of keys) {
      mycolmicro.push({
        name: schemaprops["properties"][prop]["title"],
        sortable: true,
        selector: (row, idx) => {
            if (typeof row[prop] == "boolean") {
              return row[prop] ? "yes" : "no"
            } else {
              return row[prop]
            }
        },
      });
    }

    let mydatmicro = [data["microcontroller"]]

///////////////////////////////////
////    PINS
///////////////////////////////////

  let mycolpins = [];

  const pinsschema = schema["items"]["properties"]["pins"]
  const pin_cols_schema = pinsschema["items"]["properties"]

  for (const prop of Object.keys(pin_cols_schema)) {

    mycolpins.push({
      name: pin_cols_schema[prop]["title"],
      sortable: true,

      selector: (row, idx) => {
          if (Array.isArray(row[prop])) {
            if (row[prop].length === 0)
              return " - "
            else
              return row[prop].join(', ')
          } else {
            return row[prop]
          }
      },
    });
  }

  const mydatpins = data["pins"]

  return (
    <div style={{marginRight:"20px", marginTop:"20px", marginLeft:"20px",marginBottom:"20px"}}>
      <DataTable 
        columns={mycolmicro}
        data={mydatmicro}
        style={{marginBottom: "10px", marginTop: "10px"}}
      />
      <DataTable 
        columns={mycolpins}
        data={mydatpins}
        style={{marginBottom: "10px", marginTop: "10px"}}
      />
    </div>
  );
}

  return (
    <div className="App">
      <Filter schema={schema}/>
      <DataTable
        columns={columns}
        data={data}
        pagination
        expandableRows
        expandableRowsComponent={ExpandedComponent}
        style={{width:"100vw", height:"100vh"}}
      />
    </div>
  );
}

export default App;