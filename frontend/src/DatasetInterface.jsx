import DataTable from 'react-data-table-component';
import { useState, useEffect, useRef } from 'react';

import Filter from './Filter';
import './DatasetInterface.css';

const BACKEND = process.env.REACT_APP_BACKEND_URL;

// function DatasetInterface({backend}) {
function DatasetInterface() {
  const [schema, setSchema] = useState();
  const [columns, setColumns] = useState([]);
  const [data, setData] = useState([]);

  const [filtered, setFiltered] = useState([]);
  const [pag, setPag] = useState(false);

  const downloadRef = useRef();

  const fetchdata = () => {
    // Acquire schema
    fetch(`${BACKEND}/get-schema`)
    .then((resp) => {
      resp.json().then((jsn) => {
        setSchema(jsn);

        const schemaprops = jsn["items"]["properties"]
        const cols = Object.keys(schemaprops);

        let prepped = [];
        for (const prop of cols) {
          if (prop === "pins")
            continue;

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
            wrap: true,
            center: true,
            reorder:true
          });
        }

        setColumns(prepped);
      })
    })
    .catch(() => {
      setSchema( null );
      setColumns( [] );
    })

    // Acquire json data
    fetch(`${BACKEND}/boards`)
    .then((resp) => {
      resp.json().then((jsn) => {
        // setData(jsn.data);
        setData(jsn);
      })
    })
    .catch(() => {
      setData( [] );
    })
  }

  // On load
  useEffect(() => {
    fetchdata()
  },[])

  const ExpandedComponent = ({ data }) => {
    if (!data)
      return

    if (!schema)
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
      <div
        style={{marginRight:"20px", marginTop:"50px", marginLeft:"20px", marginBottom:"50px"}}
      >
        <DataTable 
          title={"Microcontroller"}
          columns={mycolmicro}
          data={mydatmicro}
          style={{marginBottom: "10px", marginTop: "10px"}}
        />
        <DataTable 
          title={"Pins"}
          columns={mycolpins}
          data={mydatpins}
          style={{marginBottom: "10px", marginTop: "10px"}}
        />
      </div>
    );
  }

  const dlFilteredJson = (fltBy, fltTxt) => {
      fetch(`${BACKEND}/boards/filtered/json`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({'fltBy': fltBy, 'fltTxt': fltTxt})
      })
      .then((response) => {
        return response.blob()
      })
      .then((blob) => {
        const href = window.URL.createObjectURL(blob);
        const a = downloadRef.current;
        a.download = 'filtered.json';
        a.href = href;
        a.click();
        a.href = '';
      })
  }

  const dlFilteredCsv = (fltBy, fltTxt) => {
    fetch(`${BACKEND}/boards/filtered/csv`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'fltBy': fltBy, 'fltTxt': fltTxt})
    })
    .then((response) => {
      return response.blob()
    })
    .then((blob) => {
      const href = window.URL.createObjectURL(blob);
      const a = downloadRef.current;
      a.download = 'filtered.csv';
      a.href = href;
      a.click();
      a.href = '';
    })
  }

  return (
    <div className="DatasetInterface">
      <Filter
        schema={schema}
        data={data}
        applyFilter={setFiltered}
        dlFilteredJson={dlFilteredJson}
        dlFilteredCsv={dlFilteredCsv}
      />
      <a ref={downloadRef}/>
     
      <DataTable
        columns={columns}
        data={/*data*/filtered}
        pagination
        paginationResetDefaultPage={pag}
        expandableRows
        expandableRowsComponent={ExpandedComponent}
      />
    </div>
  );
}

export default DatasetInterface;