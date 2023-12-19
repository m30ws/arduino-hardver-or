import { useEffect, useState } from 'react';
import './Filter.css'

function Filter({schema, data, applyFilter, dlFilteredJson, dlFilteredCsv}) {
    const [fltBy, setFltBy] = useState("");
    const [fltTxt, setFltTxt] = useState("");
    const [optElems, setOptElems] = useState();

    const matched = (elem, flt, fltTxt) => {
        const myschema = schema["items"]["properties"]
        let fltlower = fltTxt.toLowerCase();

        // Lowpower
        if (fltlower === "yes") fltlower = true;
        if (fltlower === "no") fltlower = false;


        if (flt === "") {
            // All (*)
            const mpd = Object.entries(elem).map(([k, v]) => {

                if (k === "microcontroller") {
                    return Object.values(v).some((el) => el.toString().toLowerCase().includes(fltlower))

                } else if (k === "pins") {
                    const fm = v.flatMap((el) => {
                        return [el["pin_count"].toString(), el["pin_type"], el["pin_list"].join(",")]
                    })

                    return Object.values(fm).some((el) => el.toLowerCase().includes(fltlower))

                } else {
                    return v.toString().toLowerCase().includes(fltlower)
                }
            })
            return mpd.some((el) => el === true)
            
        } else {
            // Specific column
            if (flt === "microcontroller") {
                return Object.values(elem[flt]).some((el) => el.toString().toLowerCase().includes(fltlower))

            } else if (flt === "pins") {
                const fm = elem[flt].flatMap((el) => {
                    return [el["pin_count"].toString(), el["pin_type"], el["pin_list"].join(",")]
                })
                return Object.values(fm).some((el) => el.toLowerCase().includes(fltlower))

            } else {
                return elem[flt].toString().toLowerCase().includes(fltlower)
            }
        }
    }

    const filterData = () => {
        console.log("Filter by:", fltBy)
        console.log("Filter keyword:", fltTxt)

        const flt = (fltBy === "*") ? "" : fltBy;

        applyFilter(data.filter((elem) => {
            return  (flt === "" || elem[flt])
                        &&
                    (fltTxt === "" || matched(elem, flt, fltTxt))
        }))
    }

    useEffect(() => {
        filterData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [data, fltBy, fltTxt])

    useEffect(() => {
        filterData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
    },[])

    // on (re)load
    useEffect(() => {
        if (!schema) return

        const props = schema["items"]["properties"]
        const columns = Object.keys(props);

        const opts = columns.map((c, idx) => 
            <option id={`option-${idx}`} value={c}>
                {props[c]["title"]}
            </option>
        )

        setOptElems(opts)
    }, [schema])

    return (
        <div className="filterRoot">
            <div className="filterElem filterFont filterTitle">
                Filter results:
            </div>
            <br></br>
            <div className="filterElem">
                <input
                    className="filterFont"
                    type="search"
                    id="fltinput"
                    name="fltinput"
                    style={{width: "100%"}}
                    onChange={(ev) => {setFltTxt(ev.target.value)}}
                >
                </input>
            </div>
            <div className="filterElem">
                <select
                    className="filterFont"
                    name="columns"
                    id="columns"
                    style={{width: "100%"}}
                    onChange={(ev) => {setFltBy(ev.target.value)}}
                >
                    {/* <option value="" selected disabled={true}> -- Select filter -- </option> */}
                    <option value="*"> All (*) </option>
                    { optElems }
                </select>
            </div>
            <div className="filterElem">
                <button
                    className="filterFont"
                    style={{width: "100%"}}
                    onClick={() => {
                        let txt = fltTxt;
                        if (txt === "yes") txt = true;
                        if (txt === "no") txt = false;
                        return dlFilteredJson(fltBy, txt)
                    }}
                >
                    Download filtered JSON
                </button>
                <button
                    className="filterFont"
                    style={{width: "100%"}}
                    onClick={() => {
                        let txt = fltTxt;
                        if (txt === "yes") txt = true;
                        if (txt === "no") txt = false;
                        return dlFilteredCsv(fltBy, txt)
                    }}
                >
                    Download filtered CSV
                </button>
            </div>
            <br></br>

        </div>
    );
}

export default Filter;
